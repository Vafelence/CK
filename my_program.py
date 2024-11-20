import asyncio
import aiohttp
import datetime
from aiogram import Bot, Dispatcher, executor
from bs4 import BeautifulSoup

# Объявляем объекты бота и диспетчера
bot = Bot(token="6858480572:AAGUJwUq_UevIhrbQS6cG2nN0hfyDw8yh54")
dp = Dispatcher(bot)

internet_connection = False  # Переменная для отслеживания наличия интернет-соединения


# Функция для отправки длинных сообщений
async def send_long_message(chat_id, text):
    # Лимит сообщения в Telegram
    LIMIT = 4096

    # Разбиваем текст на части
    for i in range(0, len(text), LIMIT):
        await bot.send_message(chat_id, text[i:i + LIMIT])


async def run_task():
    global internet_connection  # Для доступа к переменной из блока except

    try:
        # Ваша логика выполнения задачи
        urls = [
            ('F1 Models',
             'https://ck-modelcars.de/ru/l/t-gesamt/k-formel1/scale-1-1-43//a-900/sort-priceup/?massstab=1&artikel=180&sort=priceup&massstab=1&hersteller=&saison=&artikel=900&sort=priceup&pmin=&pmax='),
            ('Helmets 1:5',
             'https://ck-modelcars.de/ru/l/t-suche/scale-455-1-5//a-900/sort-priceup/?s=%D1%88%D0%BB%D0%B5%D0%BC&typ=suche&massstab=455&artikel=18&sort=priceup&suche=%D1%88%D0%BB%D0%B5%D0%BC&massstab=455&hersteller=&saison=&artikel=900&sort=priceup&pmin=&pmax='),
            ('Bell Helmets', 'https://ck-modelcars.de/ru/l/t-suche/scale-12-1-2//a-900/sort-priceup/?s=bell'),
            ('Schuberth Helmets', 'https://ck-modelcars.de/ru/l/t-suche/scale-12-1-2//a-900/sort-priceup/?s=Schuberth'),
            ('All helmets',
             'https://ck-modelcars.de/ru/l/t-suche/scale-12-1-2//a-900/sort-priceup/?s=%D1%88%D0%BB%D0%B5%D0%BC&typ=suche&artikel=900&sort=priceup&suche=%D1%88%D0%BB%D0%B5%D0%BC&massstab=12&hersteller=&saison=&artikel=900&sort=priceup&pmin=&pmax='),
            ('2nd Choice',
             'https://ck-modelcars.de/ru/l/t-suche/a-900/sort-priceup/?s=choice&typ=suche&artikel=18&sort=priceup&suche=choice&massstab=&hersteller=&saison=&artikel=900&sort=priceup&pmin=&pmax='),
            ('New Models', 'https://ck-modelcars.de/ru/l/t-gesamt/k-alle/a-90/p-1/sort-new/'),
            ('Figures', 'https://ck-modelcars.de/ru/l/t-suche/k-alle/a-900/sort-priceup/?s=cartrix'),
            ('Lancer', 'https://ck-modelcars.de/ru/l/t-suche/k-alle/a-900/sort-new/?s=lancer'),
            ('Odezhda', 'https://ck-modelcars.de/ru/l/t-fanshop/k-alle/a-900/sort-priceup/'),
            ('Models 1/18', 'https://ck-modelcars.de/ru/l/t-gesamt/k-alle/scale-2-1-18/a-900/sort-priceup/pmin-30/pmax-60/'),
        ]

        new_models = {}  # Словарь для хранения новых строк
        disappeared_models = {}  # Словарь для хранения исчезнувших строк

        for text, url in urls:
            new, disappeared = await process_url(text, url)
            if new:
                new_models[text] = new
            if disappeared:
                disappeared_models[text] = disappeared

        # Формируем сообщение
        result_message = ""

        # Формируем сообщение о появлении новых моделей
        if new_models:
            result_message += "Появились новые модели:\n\n"
            for text, models in new_models.items():
                result_message += f"Для {text}:\n" + "\n".join(models) + "\n\n"

        # Добавляем пустую строку
        if new_models and disappeared_models:
            result_message += "\n"

        # Формируем сообщение об исчезнувших моделях
        if disappeared_models:
            result_message += "Исчезли модели:\n\n"
            for text, models in disappeared_models.items():
                result_message += f"Для {text}:\n" + "\n".join(models) + "\n\n"

        # Если оба словаря пусты, отправляем сообщение "Нет изменений"
        if not new_models and not disappeared_models:
            result_message = "Нет изменений"

        # Отправляем сообщение в чат, обрабатывая длину текста
        await send_long_message(-4134676016, result_message)

        # Если код выполнился успешно, устанавливаем значение internet_connection в True
        internet_connection = True

    except Exception as e:
        print(f"Ошибка: {e}")
        # Если возникла ошибка, устанавливаем значение internet_connection в False
        internet_connection = False


async def process_url(text, url):
    filename = text + '_h2_data.txt'

    # Создаем сессию с отключенной проверкой сертификатов
    connector = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:  # Создаем сессию для выполнения запроса
        async with session.get(url) as response:
            if response.status == 200:
                soup = BeautifulSoup(await response.text(), 'html.parser')
                div_liste_punkt_elements = soup.find_all(class_='div_liste_punkt')
                h2_texts = []

                for element in div_liste_punkt_elements:
                    h2_tag = element.find('h2')
                    if h2_tag:
                        h2_texts.append(h2_tag.text.strip())

                saved_h2_texts = read_from_file(filename)

                new = list(set(h2_texts) - set(saved_h2_texts))
                disappeared = list(set(saved_h2_texts) - set(h2_texts))

                write_to_file(h2_texts, filename)

                return new, disappeared

            else:
                raise Exception(f"Ошибка при получении страницы {url}: {response.status}")


def write_to_file(data, filename):
    with open(filename, 'w') as f:
        for item in data:
            f.write(item + '\n')


def read_from_file(filename):
    try:
        with open(filename, 'r') as f:
            return f.read().splitlines()
    except FileNotFoundError:
        return []


# Функция для выполнения команды /run каждые 15 минут
async def scheduled(run_task):
    global internet_connection  # Для доступа к переменной извне

    while True:
        await run_task()
        if not internet_connection:
            current_time = datetime.datetime.now().strftime("%H:%M")
            print(f"Нет интернета. Попытка подключения через 5 минут...Время проверки: {current_time}")
            await asyncio.sleep(60 * 5)  # 5 минут в секундах
        else:
            current_time = datetime.datetime.now().strftime("%H:%M")
            print(f"Интернет подключен. Проверка через 10 минут...Время проверки: {current_time}")
            await asyncio.sleep(60 * 10)  # 10 минут в секундах


# Функция для запуска асинхронной задачи запланированной команды /run
def schedule_command(dp, run_task):
    loop = asyncio.get_event_loop()
    loop.create_task(scheduled(run_task))


# Запускаем бота
if __name__ == '__main__':
    # Запуск задачи каждые 10 минут
    schedule_command(dp, run_task)
    executor.start_polling(dp, skip_updates=True)

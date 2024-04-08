# # bot_token = '6858480572:AAGUJwUq_UevIhrbQS6cG2nN0hfyDw8yh54'  # Замените 'YOUR_BOT_TOKEN' на токен вашего бота
# # chat_id = '274788783' '6858480572' '4134676016'
# https://ck-modelcars.de/ru/l/t-gesamt/k-alle/a-45/p-1/sort-new/
# import asyncio
# import aiohttp
# from bs4 import BeautifulSoup
# from aiogram import Bot
#
# # Функция для записи данных в файл
# def write_to_file(data, filename):
#     with open(filename, 'a') as f:
#         for item in data:
#             f.write(item + '\n')
#
# # Функция для чтения данных из файла
# def read_from_file(filename):
#     with open(filename, 'r') as f:
#         return f.read().splitlines()
#
# # Функция для отправки сообщения в Telegram
# async def send_telegram_message(message):
#     bot_token = '6858480572:AAGUJwUq_UevIhrbQS6cG2nN0hfyDw8yh54'  # Замените 'YOUR_BOT_TOKEN' на токен вашего бота
#     chat_id = '-4134676016'  # Замените 'YOUR_CHAT_ID' на ваш ID чата
#
#     bot = Bot(token=bot_token)
#     await bot.send_message(chat_id=chat_id, text=message)
#     await bot.close()  # Закрываем соединение с ботом
#
# async def main():
#     url = 'https://ck-modelcars.de/ru/l/t-gesamt/k-formel1/scale-1-1-43//a-900/sort-priceup/?massstab=1&artikel=180&sort=priceup&massstab=1&hersteller=&saison=&artikel=900&sort=priceup&pmin=&pmax='
#     filename = 'h2_data.txt'
#
#     async with aiohttp.ClientSession() as session:  # Создаем сессию для выполнения запроса
#         async with session.get(url) as response:
#             if response.status == 200:
#                 soup = BeautifulSoup(await response.text(), 'html.parser')
#                 div_liste_punkt_elements = soup.find_all(class_='div_liste_punkt')
#                 h2_texts = []
#
#                 for element in div_liste_punkt_elements:
#                     h2_tag = element.find('h2')
#                     if h2_tag:
#                         h2_texts.append(h2_tag.text.strip())
#
#                 write_to_file(h2_texts, filename)
#
#                 saved_h2_texts = read_from_file(filename)
#
#                 difference = list(set(h2_texts) - set(saved_h2_texts))
#
#                 message = "Разница между данными текущего запуска и предыдущего:\n"
#                 for item in difference:
#                     message += item + "\n"
#
#                 await send_telegram_message(message)
#
#                 write_to_file(h2_texts, filename)
#
#             else:
#                 await send_telegram_message("Ошибка при получении страницы: " + str(response.status))
#
# # Запуск асинхронной функции
# if __name__ == "__main__":
#     asyncio.run(main())

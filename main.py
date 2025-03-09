import os
import time

import requests
from dotenv import load_dotenv

from bot import TelegramBot

load_dotenv()

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
URL = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}

bot = TelegramBot(TELEGRAM_TOKEN)


def parse_homework_status(homework):
    homework_name = homework['homework_name']
    if homework.get('status') is None:
        time.sleep(300)
        return main()
    if homework.get('status') == 'rejected':
        verdict = 'К сожалению в работе нашлись ошибки.'

    else:
        verdict = 'Ревьюеру всё понравилось, можно приступать к следующему ' \
                  'уроку.'
    return f'У вас проверили работу "{homework_name}"!\n\n{verdict}'


def get_homework_statuses(current_timestamp):
    if current_timestamp is None:
        main()
    params = {'from_date': current_timestamp}
    try:
        homework_statuses = requests.get(URL, params=params, headers=HEADERS)
        return homework_statuses.json()
    except requests.exceptions as e:
        print(f'Проблемы с requests. Ошибка: {e}')
        time.sleep(300)
        main()


def main():
    current_timestamp = int(time.time())
    while True:
        try:
            new_homework = get_homework_statuses(current_timestamp)
            if new_homework.get('homeworks'):
                bot.send_message(
                    parse_homework_status(new_homework.get('homeworks')[0]),
                    chat_id=CHAT_ID
                )
            current_timestamp = new_homework.get(
                'current_date')
            time.sleep(300)

        except Exception as e:
            print(f'Бот упал с ошибкой: {e}')
            time.sleep(5)
            continue


if __name__ == '__main__':
    bot.send_message('Started', CHAT_ID)
    main()
from api.users import get_users_info
from api.followers import get_user_followers_info
from api.subscriptions import get_user_subscriptions_info

import time

from variables import MAX_API_DEPTH, API_SLEEP_TIME

def get_user_data(user_id: str, depth: int = 0) -> dict:
    print(f'Получение информации о пользователе {user_id}', depth)

    try:
        user_info = get_users_info(user_id)[0]
    except Exception as ex:
        print(f'Ошибка в получении данных пользователя - {ex.__str__()}')
        return {}

    time.sleep(API_SLEEP_TIME)

    print('Получение информации о фолловерах', depth)

    try:
        user_followers_info = get_user_followers_info(user_id)
    except Exception as ex:
        print(f'Ошибка в получении данных о фолловерах - {ex.__str__()}')
        user_followers_info = {}

    time.sleep(API_SLEEP_TIME)
    if depth < MAX_API_DEPTH:
        for i in range(len(user_followers_info)):
            try:
                user_followers_info[i] = get_user_data(user_followers_info[i]['id'], depth + 1)
            except Exception as ex:
                print(f'Ошибка в получении данных о фолловерах - {ex.__str__()}')
                user_followers_info[i] = {}

            time.sleep(API_SLEEP_TIME)

    print('Получение информации о подписках', depth)

    try:
        user_subscriptions_users, user_subscriptions_groups = get_user_subscriptions_info(user_id)
    except Exception as ex:
        print(f'Ошибка в получении информации о подписках - {ex.__str__()}')
        user_subscriptions_users = {}
        user_subscriptions_groups = {}

    time.sleep(API_SLEEP_TIME)
    if depth < MAX_API_DEPTH:
        for i in range(len(user_subscriptions_users)):
            try:
                user_subscriptions_users[i] = get_user_data(user_subscriptions_users[i]['id'], depth + 1)
            except Exception as ex:
                print(f'Ошибка в получении информации о подписках на пользователей - {ex.__str__()}')
                user_subscriptions_users[i] = {}
            time.sleep(API_SLEEP_TIME)

    print('Формирование общего словаря данных')
    user_info['followers'] = user_followers_info

    user_info['subscriptions'] = {}
    user_info['subscriptions']['users'] = user_subscriptions_users
    user_info['subscriptions']['groups'] = user_subscriptions_groups

    return user_info

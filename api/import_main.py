from api.users import get_users_info
from api.followers import get_user_followers_info
from api.subscriptions import get_user_subscriptions_info

from variables import MAX_API_DEPTH

def get_user_data(user_id: str, depth: int = 0) -> dict:
    print(f'Получение информации о пользователе {user_id}', depth)
    user_info = get_users_info(user_id)[0]

    print('Получение информации о фолловерах', depth)
    user_followers_info = get_user_followers_info(user_id)
    if depth < MAX_API_DEPTH:
        for i in range(len(user_followers_info)):
            user_followers_info[i] = get_user_data(user_followers_info[i]['id'], depth + 1)

    print('Получение информации о подписках', depth)
    user_subscriptions_users, user_subscriptions_groups = get_user_subscriptions_info(user_id)
    if depth < MAX_API_DEPTH:
        for i in range(len(user_subscriptions_users)):
            user_subscriptions_users[i] = get_user_data(user_subscriptions_users[i]['id'], depth + 1)


    print('Формирование общего словаря данных')
    user_info['followers'] = user_followers_info

    user_info['subscriptions'] = {}
    user_info['subscriptions']['users'] = user_subscriptions_users
    user_info['subscriptions']['groups'] = user_subscriptions_groups

    return user_info

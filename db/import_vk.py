from json_functions import read_json
from db.queries import add_followers, add_subscription_users, add_subscription_groups


def form_user_dict(data: dict) -> dict:
    if data == {}:
        return {}

    user_dict = {}
    user_dict['id'] = data['id']
    user_dict['screen_name'] = data['screen_name']
    user_dict['name'] = data['first_name'] + ' ' + data['last_name']
    user_dict['sex'] = data['sex']
    if 'city' in data:
        user_dict['home_town'] = data['city']['title']
    else:
        user_dict['home_town'] = ''

    return user_dict


def form_group_dict(data: dict) -> dict:
    if data == {}:
        return {}

    group_dict = {}
    group_dict['id'] = data['id']
    group_dict['name'] = data['name']
    group_dict['screen_name'] = data['screen_name']

    return group_dict


def import_follower(data: dict) -> None:
    if 'followers' in data:
        for follower in data['followers']:
            user_info = form_user_dict(data)
            follower_info = form_user_dict(follower)
            if user_info != {} and follower_info != {}:
                add_followers(user_info, follower_info)
                import_follower(follower)

                if 'subscriptions' in follower:
                    import_subscription_user(follower)
                    import_subscription_group(follower)


def import_subscription_user(data: dict) -> None:
    if 'users' in data['subscriptions']:
        for subscription in data['subscriptions']['users']:
            user_info = form_user_dict(data)
            subscription_info = form_user_dict(subscription)
            if user_info != {} and subscription_info != {}:
                add_subscription_users(user_info, subscription_info)

                import_follower(subscription)
                if 'subscriptions' in subscription:
                    import_subscription_user(subscription)


def import_subscription_group(data: dict) -> None:
    if 'groups' in data['subscriptions']:
        for subscription in data['subscriptions']['groups']:
            user_info = form_user_dict(data)
            subscription_info = form_group_dict(subscription)
            if user_info != {} and subscription_info != {}:
                add_subscription_groups(user_info, subscription_info)


def run_import(filepath: str) -> bool:
    try:
        data = read_json(filepath)
    except Exception as ex:
        print(f'Не удалось прочитать указанный файл {filepath}, {ex.__str__()}')
        return False

    import_follower(data)
    import_subscription_user(data)

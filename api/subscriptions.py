import requests

from variables import ACCESS_TOKEN, SERVER_ADDRESS_OPTIONS, TESTED_VK_API_VERSION
from check import check_response
from api.users import get_users_info
from api.groups import get_groups_info


def get_user_subscriptions(user_id: str) -> dict:
    for server_address in SERVER_ADDRESS_OPTIONS:
        response = requests.post(
            f'https://{server_address}/method/users.getSubscriptions?user_id={user_id}&v={TESTED_VK_API_VERSION}',
            headers={'Content-Type': 'multipart/form-data', 'Authorization': 'Bearer ' + ACCESS_TOKEN}
        )

        if check_response(response):
            return response.json()['response']

    return {}


def get_user_subscriptions_info(user_id: str) -> tuple[dict, dict]:
    subscriptions = get_user_subscriptions(user_id)

    user_subscriptions_ids = subscriptions['users']['items']
    user_subscriptions_ids = [str(id) for id in user_subscriptions_ids]

    group_subscriptions_ids = subscriptions['groups']['items']
    group_subscriptions_ids = [str(id) for id in group_subscriptions_ids]

    user_subscriptions_info = get_users_info(','.join(user_subscriptions_ids))
    group_subscriptions_info = get_groups_info(','.join(group_subscriptions_ids))

    return user_subscriptions_info, group_subscriptions_info

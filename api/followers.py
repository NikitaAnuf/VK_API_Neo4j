import requests

from variables import ACCESS_TOKEN, SERVER_ADDRESS_OPTIONS, TESTED_VK_API_VERSION
from check import check_response
from api.users import get_users_info


def get_user_followers_ids(user_id: str) -> dict:
    for server_address in SERVER_ADDRESS_OPTIONS:
        response = requests.post(
            f'https://{server_address}/method/users.getFollowers?user_id={user_id}&v={TESTED_VK_API_VERSION}',
            headers={'Content-Type': 'multipart/form-data', 'Authorization': 'Bearer ' + ACCESS_TOKEN}
        )

        if check_response(response):
            return response.json()['response']

    return {}


def get_user_followers_info(user_id: str) -> dict:
    ids = get_user_followers_ids(user_id)['items']
    ids = [str(id) for id in ids]

    return get_users_info(','.join(ids))

import requests

from variables import ACCESS_TOKEN, SERVER_ADDRESS_OPTIONS, TESTED_VK_API_VERSION
from check import check_response


def get_users_info(user_ids: str) -> dict:
    for server_address in SERVER_ADDRESS_OPTIONS:
        response = requests.post(
            f'https://{server_address}/method/users.get?user_ids={user_ids}&fields=screen_name,sex,city&v={TESTED_VK_API_VERSION}',
            headers={'Content-Type': 'multipart/form-data', 'Authorization': 'Bearer ' + ACCESS_TOKEN}
        )
        if check_response(response):
            return response.json()['response']

    return {}

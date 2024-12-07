import requests

from variables import ACCESS_TOKEN, SERVER_ADDRESS_OPTIONS, TESTED_VK_API_VERSION
from check import check_response


def get_groups_info(group_ids: str) -> dict:
    for server_address in SERVER_ADDRESS_OPTIONS:
        response = requests.post(
            f'https://{server_address}/method/groups.getById?group_ids={group_ids}&v={TESTED_VK_API_VERSION}',
            headers={'Content-Type': 'multipart/form-data', 'Authorization': 'Bearer ' + ACCESS_TOKEN}
        )

        if check_response(response):
            return response.json()['response']['groups']

    return {}

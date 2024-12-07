import requests


def check_response(response: requests.Response) -> bool:
    if response.status_code == 200:
        return True
    else:
        print(f'Ошибка в запросе - код {response.status_code}')
        return False

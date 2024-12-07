from prettytable import PrettyTable

from typing import Literal


def print_count(count: int, type: Literal['user', 'group']) -> None:
    if type == 'user':
        res = 'Всего пользователей: '
    else:
        res = 'Всего групп: '
    res += str(count)
    print(res)


def print_followed_users(users: list[dict]) -> None:
    if len(users) > 0:
        table = PrettyTable(['ID', 'Name', 'Screen name', 'Hometown', 'Sex', 'Number of followers'])

        for user in users:
            table.add_row([user['User']['id'], user['User']['name'], user['User']['screen_name'], user['User']['home_town'],
                           user['User']['sex'], user['number_of_followers']])

        print(table)

    else:
        print('Нет пользователей с фолловерами')


def print_subscribed_groups(groups: list[dict]) -> None:
    if len(groups) > 0:
        table = PrettyTable(['ID', 'Name', 'Screen name', 'Number of subscribers'])

        for group in groups:
            table.add_row([group['Group']['id'], group['Group']['name'], group['Group']['screen_name'],
                           group['number_of_subscribers']])

        print(table)

    else:
        print('Нет групп с подписчиками')


def print_mutual_followers(users: list[dict]) -> None:
    if len(users) > 0:
        table = PrettyTable(['User 1 ID', 'User 1 name', 'User 1 screen name', 'User 1 hometown', 'User 1 sex',
                             'User 2 ID', 'User 2 name', 'User 2 screen name', 'User 2 hometown', 'User 2 sex'])

        for user in users:
            table.add_row([user['User1']['id'], user['User1']['name'], user['User1']['screen_name'],
                           user['User1']['home_town'], user['User1']['sex'], user['User2']['id'], user['User2']['name'],
                           user['User2']['screen_name'], user['User2']['home_town'], user['User2']['sex']])

        print(table)

    else:
        print('Среди пользователей нет взаимных фолловеров')

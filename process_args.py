import argparse
import datetime
import os
import logging
from logging import exception

from api.import_main import get_user_data
from json_functions import write_json

from db.import_vk import run_import
from db.queries import count_users, count_groups, top_followed_users, top_subscribed_groups, mutual_followers
from db.return_query_results import print_count, print_followed_users, print_subscribed_groups, print_mutual_followers

from logger import get_logger

from variables import BASE_VK_USER_ID, RESULTS_BASE_DIR, BASE_RESULT_FILE


def create_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    # Аргумент для задания режима работы приложения
    parser.add_argument('--mode', '-m', type=str, default='query')

    # Аргументы для записи данных из VK API в JSON-файл
    parser.add_argument('--userid', '-u', type=str, default=BASE_VK_USER_ID)
    # Этот аргумент также работает для импорта в Neo4j
    parser.add_argument('--filepath', '-f', type=str, default=None)

    # Аргумент для определения вида запроса
    parser.add_argument('--type', '-t', type=str, default='count')

    # Для запросов типа count - подсчёт всех пользователей и групп и на выборку узлов с наибольшим количеством связей
    parser.add_argument('--nodetype', '-n', type=str, default='user')

    # Для запросов на выборку узлов с наибольшим количеством связей
    parser.add_argument('--topn', type=int, default=5)

    return parser


def print_wrong_args(general_logger: logging.Logger) -> None:
    print('В командную строку введены неправильные аргументы')
    general_logger.info('В командную строку введены неправильные аргументы')


def run() -> None:
    print('Начало работы')

    print('Обработка параметров командной строки')

    parser = create_argparser()
    args = parser.parse_args()

    general_logger = get_logger('general')

    if args.mode == 'api':
        general_logger.info('Вызов загрузки данных из VK API')

        user_id = args.userid

        if args.filepath is None:
            filepath = BASE_RESULT_FILE
        else:
            if args.filepath.endswith('.json'):
                filepath = args.filepath
            else:
                filepath = os.path.join(args.filepath, datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '.json')

        api_logger = get_logger('api')
        api_logger.info('Начало получения данных из VK API')

        user_info = {}
        try:
            user_info = get_user_data(user_id)
        except Exception as ex:
            print(f'Ошибка в получении информации из VK API - {ex.__str__()}')
            api_logger.warning(f'Ошибка в получении информации из VK API - {ex.__str__()}')

        api_logger.info('Конец получения данных из VK API')

        try:
            write_json(user_info, filepath)
        except Exception as ex:
            print(f'Ошибка в записи JSON-файла - {ex.__str__()}')
            api_logger.error(f'Ошибка в записи JSON-файла - {ex.__str__()}')

        api_logger.info('JSON-файл успешно записан')


    elif args.mode == 'import':
        general_logger.info('Вызов загрузки данных в Neo4j')

        if args.filepath.endswith('.json'):
            filepath = args.filepath
        else:
            files = [f for f in os.listdir(RESULTS_BASE_DIR) if os.path.isfile(os.path.join(RESULTS_BASE_DIR, f)) and f.endswith('.json')]
            files.sort(reverse=True)
            filepath = os.path.join(RESULTS_BASE_DIR, files[0])

        import_logger = get_logger('import')
        import_logger.info('Начало импорта данных в Neo4j')

        try:
            run_import(filepath)
        except Exception as ex:
            print(f'Ошибка в импорте данных в Neo4j - {ex.__str__()}')
            import_logger.error(f'Ошибка в импорте данных в Neo4j - {ex.__str__()}')

        import_logger.info('Конец импорта данных в Neo4j')

    elif args.mode == 'query':
        general_logger.info('Запрос к Neo4j')

        query_logger = get_logger('query')

        if args.type == 'count':
            query_logger.info('Вызван запрос типа count')

            try:
                if args.nodetype == 'user':
                    print_count(count_users(), 'user')
                elif args.nodetype == 'group':
                    print_count(count_groups(), 'group')
                else:
                    print_wrong_args(general_logger)
            except Exception as ex:
                print(f'Ошибка в выполнении запроса типа count - {ex.__str__()}')
                query_logger.error(f'Ошибка в выполнении запроса типа count - {ex.__str__()}')

        elif args.type == 'top':
            query_logger.info('Вызван запрос типа top')

            try:
                if not isinstance(args.topn, int) or args.topn <= 0:
                    print_wrong_args(general_logger)

                else:
                    if args.nodetype == 'user':
                        print_followed_users(top_followed_users(args.topn))
                    elif args.nodetype == 'group':
                        print_subscribed_groups(top_subscribed_groups(args.topn))
                    else:
                        print_wrong_args(general_logger)
            except Exception as ex:
                print(f'Ошибка в выполнении запроса типа top - {ex.__str__()}')
                query_logger.error(f'Ошибка в выполнении запроса типа top - {ex.__str__()}')

        elif args.type == 'mutual':
            try:
                print_mutual_followers(mutual_followers())
            except Exception as ex:
                print(f'Ошибка в выполнении запроса типа mutual - {ex.__str__()}')
                query_logger.error(f'Ошибка в выполнении запроса типа mutual - {ex.__str__()}')

        else:
            print_wrong_args(general_logger)

    else:
        print_wrong_args(general_logger)

    general_logger.info('Выполнение программы завершено без ошибок')

    print('Работа закончена')

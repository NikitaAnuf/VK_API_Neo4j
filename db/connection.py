from neo4j import GraphDatabase
from dotenv import load_dotenv

import os

class Connection:
    load_dotenv()

    __DB_HOST = os.getenv("NEO4J_HOST")
    __DB_PORT = os.getenv("NEO4J_PORT")
    __DB_USER = os.getenv("NEO4J_USER")
    __DB_PASSWORD = os.getenv("NEO4J_PASSWORD")
    __DB_NAME = os.getenv("NEO4J_NAME")

    URI = f'neo4j://{__DB_HOST}:{__DB_PORT}'
    AUTH = (__DB_USER, __DB_PASSWORD)

    driver = GraphDatabase.driver(URI, auth=AUTH)
    session = driver.session(database=__DB_NAME)

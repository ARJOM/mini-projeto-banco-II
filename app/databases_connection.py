import os
import psycopg2
import redis
from pymongo import MongoClient
from dotenv import load_dotenv


# Carregando dados do ambiente virtual
load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
DB_NAME = os.getenv("DB_NAME")
PSQL_HOST = os.getenv("PSQL_HOST")
PSQL_USER = os.getenv("PSQL_USER")
PSQL_PASSWORD = os.getenv("PSQL_PASSWORD")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = os.getenv("MONGO_PORT")


conn_psql = psycopg2.connect(f"dbname={DB_NAME} user={PSQL_USER} password={PSQL_PASSWORD} host={PSQL_HOST}")
conn_redis = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

client = MongoClient(MONGO_HOST, MONGO_PORT)
conn_mongo = client[MONGO_DB_NAME]

import os
import sys
import time
import logging

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

from models import Base

LOGGER = logging.getLogger(__name__)

DB_HOST = os.getenv("DATABASE_HOST", "localhost")
DB_PORT = os.getenv("DATABASE_PORT", 5432)
DB_NAME = os.getenv("DATABASE_NAME", "crypto")
DB_USER = os.getenv("DATABASE_USER", "crypto")
DB_PASSWORD = os.getenv("DATABASE_PASSWORD", "crypto")

print(f"Host: {DB_HOST}")
print(f"Port: {DB_PORT}")
print(f"Name: {DB_NAME}")
print(f"User: {DB_USER}")
print(f"Password: {DB_PASSWORD}")
ENGINE = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

def init_db():
    max_retries = 30
    retry_interval = 1

    for _ in range(max_retries):
        try:
            Base.metadata.create_all(ENGINE, checkfirst=True)
            break
        except OperationalError as e:
            LOGGER.warning(f"Error connecting to the database: {e}")
            LOGGER.warning("Retrying in {} seconds...".format(retry_interval))
            time.sleep(retry_interval)
    else:
        LOGGER.error("Failed to establish a connection within the specified time.")

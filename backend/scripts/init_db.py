"""Database initialization script."""

from database import init_db
from modules.date_extractor import date_extractor
from loguru import logger


def initialize_database():
    """
    Initialize the database and create all tables.
    """
    logger.info("Initializing database...")
    init_db()
    logger.info("Database initialization complete")


if __name__ == "__main__":
    initialize_database()

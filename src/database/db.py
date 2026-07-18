"""
Database Connection Manager

Handles all low-level SQLite database operations.
"""

import sqlite3

from config.config import Config
from src.utils.logger import get_logger

logger = get_logger(__name__)


class Database:
    """
    SQLite Database Manager.
    """

    def __init__(self):
        """
        Create a database connection.
        """

        self.connection = sqlite3.connect(
            Config.DATABASE_PATH
        )

        self.connection.execute("PRAGMA foreign_keys = ON")

        # Return rows as dictionaries instead of tuples
        self.connection.row_factory = sqlite3.Row

        self.cursor = self.connection.cursor()

        logger.info("Connected to SQLite database.")

    def execute(self, query, params=()):
        """
        Execute a single SQL query.
        """

        self.cursor.execute(query, params)
        self.connection.commit()

    def executemany(self, query, params):
        """
        Execute multiple SQL statements.
        """

        self.cursor.executemany(query, params)
        self.connection.commit()

    def fetchone(self):
        """
        Fetch one row.
        """

        return self.cursor.fetchone()

    def fetchall(self):
        """
        Fetch all rows.
        """

        return self.cursor.fetchall()

    def begin_transaction(self):
        """
        Begin a database transaction.
        """

        self.connection.execute("BEGIN")

    def commit(self):
        """
        Commit the current transaction.
        """

        self.connection.commit()

    def rollback(self):
        """
        Roll back the current transaction.
        """

        self.connection.rollback()

    def close(self):
        """
        Close the database connection.
        """

        if self.connection:

            self.connection.close()

            logger.info("Database connection closed.")
"""
Database Connection Manager

Handles all low-level SQLite database operations.
"""

import sqlite3
import threading

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

        self.connection = sqlite3.connect(Config.DATABASE_PATH, check_same_thread=False)

        self.connection.execute("PRAGMA foreign_keys = ON")

        # Return rows as dictionaries instead of tuples
        self.connection.row_factory = sqlite3.Row

        # Use thread-local storage for cursors to support concurrent threaded asyncio calls
        self.local = threading.local()

        logger.info("Connected to SQLite database.")

    def _get_cursor(self):
        if not hasattr(self.local, "cursor"):
            self.local.cursor = self.connection.cursor()
        return self.local.cursor

    def execute(self, query, params=()):
        """
        Execute a single SQL query.
        """
        cursor = self._get_cursor()
        cursor.execute(query, params)
        self.connection.commit()

    def executemany(self, query, params):
        """
        Execute multiple SQL statements.
        """
        cursor = self._get_cursor()
        cursor.executemany(query, params)
        self.connection.commit()

    def fetchone(self):
        """
        Fetch one row.
        """

        return self._get_cursor().fetchone()

    def fetchall(self):
        """
        Fetch all rows.
        """

        return self._get_cursor().fetchall()

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

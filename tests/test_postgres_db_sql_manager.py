import unittest

from core import app_env
from core.utils.databases.managers.sql.postgres_db_manager import (
    PostgresDbManager,
)


class TestPostgresDbManager(unittest.TestCase):
    def setUp(self) -> None:
        """Init the test configuration."""

        self.hostname = app_env["HOSTNAME"]
        self.database = app_env["DB_NAME"]
        self.user = app_env["DB_USER"]
        self.password = app_env["DB_PASSWORD"]
        self.postgres_db_manager = PostgresDbManager(
            host=self.hostname,
            database=self.database,
            user=self.user,
            password=self.password,
        )

    def test_db_manager_initialized(self):
        """Test a service postgres database manager is available."""

        self.assertIsNotNone(
            self.postgres_db_manager.host, "The hostname is empty"
        )
        self.assertIsNotNone(
            self.postgres_db_manager.database, "The database is empty"
        )
        self.assertIsNotNone(
            self.postgres_db_manager.user, "The username is empty"
        )
        self.assertIsNotNone(
            self.postgres_db_manager.password, "the password is empty"
        )
        self.assertIsNotNone(
            self.postgres_db_manager.port, "the port is empty"
        )
        self.assertEqual(
            self.postgres_db_manager.mode, "SQL", "the mode is incorrect"
        )

    def test_db_connect(self):
        """Test the connection with service postgres database manager."""

        self.assertTrue(
            self.postgres_db_manager.connect(),
            "The connection to the postgres db failed",
        )
        self.assertIsNotNone(
            self.postgres_db_manager.connection,
            "the connection property is empty",
        )

    def test_db_disconnect(self):
        """Test the disconnection to service postgres database manager."""

        self.postgres_db_manager.connect()
        self.assertTrue(
            self.postgres_db_manager.disconnect(),
            "The disconnection to the postgres db failed",
        )
        self.assertIsNone(
            self.postgres_db_manager.connection,
            "the connection property is not empty",
        )

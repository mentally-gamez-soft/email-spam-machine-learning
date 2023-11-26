import unittest

from core import app_env
from core.utils.constants import NOSQL_MODE, SQL_MODE
from core.utils.databases.managers.factory.factory_db_manager import (
    FactoryDbManager,
)


class TestFactoryDbManager(unittest.TestCase):
    def setUp(self) -> None:
        self.hostname = app_env["HOSTNAME"]
        self.database = app_env["DB_NAME"]
        self.user = app_env["DB_USER"]
        self.password = app_env["DB_PASSWORD"]

    def test_factory_postgres_db_manager_initialized(self):
        """Test factory for postgres database manager."""

        postgres_db_manager = FactoryDbManager.new_instance_db_manager(
            mode=SQL_MODE,
            host=self.hostname,
            database=self.database,
            user=self.user,
            password=self.password,
        )

        self.assertIsNotNone(postgres_db_manager.host, "The hostname is empty")
        self.assertIsNotNone(
            postgres_db_manager.database, "The database is empty"
        )
        self.assertIsNotNone(postgres_db_manager.user, "The username is empty")
        self.assertIsNotNone(
            postgres_db_manager.password, "the password is empty"
        )
        self.assertIsNotNone(postgres_db_manager.port, "the port is empty")
        self.assertEqual(
            postgres_db_manager.mode, "SQL", "the mode is incorrect"
        )

    @unittest.skip("The nosql MongoDB source is not ready yet !!!!")
    def test_factory_mongo_db_manager_initialized(self):
        """Test factory for mongoDB database manager."""

        mongo_db_manager = FactoryDbManager.new_instance_db_manager(
            mode=NOSQL_MODE,
            host=self.hostname,
            database=self.database,
            user=self.user,
            password=self.password,
        )

        self.assertIsNotNone(mongo_db_manager.host, "The hostname is empty")
        self.assertIsNotNone(
            mongo_db_manager.database, "The database is empty"
        )
        self.assertIsNotNone(mongo_db_manager.user, "The username is empty")
        self.assertIsNotNone(
            mongo_db_manager.password, "the password is empty"
        )
        self.assertIsNotNone(mongo_db_manager.port, "the port is empty")
        self.assertEqual(
            mongo_db_manager.mode, "NOSQL", "the mode is incorrect"
        )

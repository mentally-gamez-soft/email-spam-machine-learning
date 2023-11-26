import unittest

from core import app_env
from core.utils.databases.managers.nosql.mongo_db_manager import MongoDbManager


@unittest.skip("The nosql MongoDB source is not ready yet !!!!")
class TestMongoDbManager(unittest.TestCase):
    def setUp(self) -> None:
        self.hostname = app_env["HOSTNAME"]
        self.database = app_env["DB_NAME"]
        self.user = app_env["DB_USER"]
        self.password = app_env["DB_PASSWORD"]
        self.mongo_db_manager = MongoDbManager(
            host=self.hostname,
            database=self.database,
            user=self.user,
            password=self.password,
        )

    def test_db_manager_initialized(self):
        """Test a service mongoDB database manager is available."""

        self.assertIsNotNone(
            self.mongo_db_manager.host, "The hostname is empty"
        )
        self.assertIsNotNone(
            self.mongo_db_manager.database, "The database is empty"
        )
        self.assertIsNotNone(
            self.mongo_db_manager.user, "The username is empty"
        )
        self.assertIsNotNone(
            self.mongo_db_manager.password, "the password is empty"
        )
        self.assertIsNotNone(self.mongo_db_manager.port, "the port is empty")
        self.assertEquals(
            self.mongo_db_manager.mode, "NOSQL", "the mode is incorrect"
        )

    def test_db_connect(self):
        """Test the connection with service mongoDB database manager."""

        self.assertTrue(
            self.mongo_db_manager.connect(),
            "The connection to the mongo db failed",
        )
        self.assertIsNotNone(
            self.mongo_db_manager.connection,
            "the connection property is empty",
        )

    def test_db_disconnect(self):
        """Test the disconnection to service mongoDB database manager."""

        self.mongo_db_manager.connect()
        self.assertTrue(
            self.mongo_db_manager.disconnect(),
            "The disconnection to the mongo db failed",
        )
        self.assertIsNone(
            self.mongo_db_manager.connection,
            "the connection property is not empty",
        )

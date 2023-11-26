"""Manager for the database Mongo."""

from pymongo import MongoClient

from core.utils.constants import NOSQL_MODE
from core.utils.databases.managers.interface_db_manager import (
    InterfaceDbManager,
)


class MongoDbManager(InterfaceDbManager):
    """Concrete database manager specifical for Mongo."""

    def __init__(self, **kwargs) -> None:
        """Init an instance of the Mongo DB manager.

        Args:
            **host (str): The hostname for the service
            **port (int): The port for the service
            **database (str): The databse name service
            **user (str): username
            **password (str): password
        """
        super().__init__(**kwargs)
        self.client = None
        self.mode = NOSQL_MODE

    def connect(self, **kwargs) -> bool:
        """Open a connection to the database Mongo.

        Args:
            **host (str): The hostname for the service or None
            **port (int): The port for the service or None
            **database (str): The databse name service or None
            **user (str): username or None
            **password (str): password or None

        Returns:
            bool: return True if the connection is established, False otherwise.
        """
        # login = os.getenv('MONGO_USER')
        # password = os.getenv('MONGO_PASSWORD')
        self.set_hostname(kwargs.get("host"))
        self.set_port(kwargs.get("port"))
        self.set_dbname(kwargs.get("database"))
        self.set_credentials(kwargs.get("user"), kwargs.get("password"))
        # self.client = MongoClient("mongo-db",username=login,password=password,authSource="spam_ham")
        self.connection = MongoClient(
            "mongodb://{}:{}@{}:{}/{}?ssl=false".format(
                self.user, self.password, self.host, self.port, self.database
            )
        )

        if self.connection:
            return True

        return False

    def disconnect(self) -> bool:
        """Close the connection to the Mongo database.

        Returns:
            bool: True if the connection is closed, False otherwise
        """
        self.connection.close()
        self.connection = None
        return True

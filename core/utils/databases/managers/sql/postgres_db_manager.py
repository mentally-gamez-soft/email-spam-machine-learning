"""Manager for the database postgres SQL."""

import psycopg2

from core.utils.constants import SQL_MODE
from core.utils.databases.managers.interface_db_manager import (
    InterfaceDbManager,
)


class PostgresDbManager(InterfaceDbManager):
    """Concrete database manager specifical for postgres SQL."""

    def __init__(self, **kwargs) -> None:
        """Init an instance of the postgres SQL manager.

        Args:
            **host (str): The hostname for the service
            **port (int): The port for the service
            **database (str): The databse name service
            **user (str): username
            **password (str): password
        """
        super().__init__(**kwargs)

        self.mode = SQL_MODE

    def connect(self, **kwargs) -> bool:
        """Open a connection to the database postgres SQL.

        Args:
            **host (str): The hostname for the service or None
            **port (int): The port for the service or None
            **database (str): The databse name service or None
            **user (str): username or None
            **password (str): password or None

        Returns:
            bool: return True if the conection is established, False otherwise.
        """
        self.set_hostname(kwargs.get("host"))
        self.set_port(kwargs.get("port"))
        self.set_dbname(kwargs.get("database"))
        self.set_credentials(kwargs.get("user"), kwargs.get("password"))

        self.connection = psycopg2.connect(
            host=self.host,
            database=self.database,
            port=self.port,
            user=self.user,
            password=self.password,
        )

        if self.connection is not None:
            self.connection.autocommit = True
            return True

        return False

    def disconnect(self) -> bool:
        """Close the connection to the postgres SQL database.

        Returns:
            bool: True if the connection is closed, False otherwise
        """
        if self.connection is not None:
            self.connection = self.connection.close()

        if self.connection is None:
            return True

        return False

"""Interface for all the databas managers."""

class InterfaceDbManager:
    """Super class for the database managers."""

    def set_hostname(self, host: str):
        """Set the hostname of the DB service.

        Args:
            host (str): the hostname for the database service
        """
        self.host = host if host is not None else self.host

    def set_port(self, port: int):
        """Set the port for the DB service.

        Args:
            port (int): the port for the database service
        """
        self.port = port if port is not None else self.port

    def set_dbname(self, db: str):
        """Set the name for the DB service.

        Args:
            db (str): The name of the databse service
        """
        self.database = db if db is not None else self.database

    def set_credentials(self, username: str, password: str):
        """Set redentials for the DB service.

        Args:
            username (str): the username for the database service
            password (str): the password for the database service
        """
        self.user = username if username is not None else self.user
        self.password = password if password is not None else self.password

    def __init__(self, *args, **kwargs) -> None:
        """Init an instance of DB service.

        Args:
            **host (str): The hostname for the service
            **port (int): The port for the service
            **database (str): The databse name service
            **user (str): username
            **password (str): password
        """
        self.host = None
        self.set_hostname(kwargs.get("host"))

        self.port = 5432
        self.set_port(kwargs.get("port"))

        self.database = None
        self.set_dbname(kwargs.get("database"))

        self.user = None
        self.password = None
        self.set_credentials(kwargs.get("user"), kwargs.get("password"))

        self.connection = None

        self.mode = None

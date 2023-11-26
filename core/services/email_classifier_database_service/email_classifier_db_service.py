"""Define the superclass of the service for databases connection.

This database service will work with SGBDR sql, nosql like Mongo and ORM tools like SQLAlchemy.
It is an abstraction to the mentionned database systems.
"""

from core.utils.constants import NOSQL_MODE, SQL_MODE


class EmailClassifierDbService:
    """Define the super class for a service of type database."""

    def __is_valid_manager(self) -> bool:
        if self.db_manager is None:
            return False
        return True

    def is_valid(self) -> bool:
        """Indicate if the manager is still valid to use.

        Returns:
            bool: True when the manager can be used. False otherwise.
        """
        return self.__is_valid_manager()

    def get_mode(self) -> str:
        """Define for which kind of database this manager is used for.

        Returns:
            str: 'NOSQL' for nosql db / 'SQL' for sql db / 'ORM' in case of SQLAchemy
        """
        return self.db_manager.mode

    def open_connection(self):
        """Open the database connection.

        Returns:
            Any: The connection object for this manager.
        """
        if self.__is_valid_manager():
            self.db_manager.connect()
        return self.db_manager.connection

    def close_connection(self):
        """Close the connection to the database.

        Returns:
            Any: The object of connection. Expected to be None.
        """
        if self.__is_valid_manager():
            self.db_manager.disconnect()
        return self.db_manager.connection

    def __is_connected(self) -> bool:
        if self.db_manager.connection:
            return True
        return False

    def __init__(self, **kwargs) -> None:
        """Instanciate the superclass Service."""
        self.db_manager = (
            kwargs.get("db_manager")
            if kwargs.get("db_manager") is not None
            else None
        )

    def record_spam_email(self, **kwargs) -> int:
        """Save an email as a spam in the database.

        Returns:
            int: The id of the newly created record.
        """
        ip_address = kwargs.get("ip_user")["ip_address"]
        country_code = kwargs.get("ip_user")["country_code"]
        country_name = kwargs.get("ip_user")["country_name"]
        region = kwargs.get("ip_user")["region"]
        latitude = kwargs.get("ip_user")["latitude"]
        longitude = kwargs.get("ip_user")["longitude"]
        email = kwargs.get("email")

        new_record_id = -1

        if not self.__is_connected():
            self.open_connection()

            if self.db_manager.mode == SQL_MODE:
                new_record_id = self.record_spam_email_with_sql(
                    email=email,
                    user_ip_address=ip_address,
                    country_code=country_code,
                    country_name=country_name,
                    region=region,
                    latitude=latitude,
                    longitude=longitude,
                )
                self.close_connection()
            elif self.db_manager.mode == NOSQL_MODE:
                new_record_id = self.record_spam_email_with_nosql(
                    email, ip_address
                )

        return new_record_id

    def record_ham_email(self, **kwargs) -> int:
        """Save an email as a ham in the database.

        Returns:
            int: The id of the newly created record.
        """
        ip_address = kwargs.get("ip_user")["ip_address"]
        country_code = kwargs.get("ip_user")["country_code"]
        country_name = kwargs.get("ip_user")["country_name"]
        region = kwargs.get("ip_user")["region"]
        latitude = kwargs.get("ip_user")["latitude"]
        longitude = kwargs.get("ip_user")["longitude"]
        email = kwargs.get("email")

        new_record_id = -1

        if not self.__is_connected():
            self.open_connection()

            if self.db_manager.mode == SQL_MODE:
                new_record_id = self.record_ham_email_with_sql(
                    email=email,
                    user_ip_address=ip_address,
                    country_code=country_code,
                    country_name=country_name,
                    region=region,
                    latitude=latitude,
                    longitude=longitude,
                )
                self.close_connection()
            elif self.db_manager.mode == NOSQL_MODE:
                new_record_id = self.record_ham_email_with_nosql(
                    email, ip_address
                )

        return new_record_id

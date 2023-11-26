"""Manage the CRUD operations for the service against the pgsql database."""

from core.services.email_classifier_database_service.email_classifier_db_service import (
    EmailClassifierDbService,
)
from core.utils.databases.managers.sql.postgres_db_manager import (
    PostgresDbManager,
)


class EmailClassifierDbSqlService(EmailClassifierDbService):
    """Manage the postgre SQL database service.

    Args:
        EmailClassifierDbService (_type_): The superclass for the manager.
    """

    def __init__(self, **kwargs) -> None:
        """Instantiate the service."""
        super().__init__(**kwargs)

    def __record_user_with_sql(
        self,
        connection,
        user_ip_address: str,
        country_code: str,
        country_name: str,
        region: str,
        latitude=None,
        longitude=None,
    ) -> int:
        new_user_id = -1
        sql_user_query = (
            "INSERT INTO USERS"
            ' ("IP_ADDRESS_ORIGIN","COUNTRY_CODE","COUNTRY_NAME","REGION","LATITUDE","LONGITUDE")'
            ' VALUES ( %s,%s,%s,%s,%s,%s ) RETURNING "ID";'
        )
        cursor = connection.cursor()  # ('c_insert_user')
        cursor.execute(
            sql_user_query,
            (
                user_ip_address,
                country_code,
                country_name,
                region,
                latitude,
                longitude,
            ),
        )
        new_user_id = cursor.fetchone()[0]
        cursor.close()
        return new_user_id

    def __record_spam_email_with_sql(
        self, connection, email: str, user_id: int
    ) -> int:
        new_spam_id = -1
        sql_spam_query = (
            'INSERT INTO SPAM_EMAIL ("EMAIL","USER_ID") VALUES (%s,%s)'
            ' RETURNING "ID";'
        )
        cursor = connection.cursor()
        cursor.execute(
            sql_spam_query,
            (
                email,
                user_id,
            ),
        )
        new_spam_id = cursor.fetchone()[0]
        cursor.close()
        return new_spam_id

    def __record_ham_email_with_sql(
        self, connection, email: str, user_id: int
    ) -> int:
        new_ham_id = -1
        sql_spam_query = (
            'INSERT INTO HAM_EMAIL ("EMAIL","USER_ID") VALUES (%s,%s)'
            ' RETURNING "ID";'
        )
        cursor = connection.cursor()
        cursor.execute(
            sql_spam_query,
            (
                email,
                user_id,
            ),
        )
        new_ham_id = cursor.fetchone()[0]
        cursor.close()
        return new_ham_id

    def record_spam_email_with_sql(
        self,
        email: str,
        user_ip_address: str,
        country_code: str = None,
        country_name: str = None,
        region: str = None,
        latitude=None,
        longitude=None,
    ) -> int:
        """Store the email as a spam in the SQL database.

        Args:
            email (str): the spam message to store.
            user_ip_address (str): the IP v4 ip address of the end user.
            country_code (str, optional): The country code for the geolocation of the end user. Defaults to None.
            country_name (str, optional): The country for the geolocation of the end user. Defaults to None.
            region (str, optional): The region for the geolocation of the end user. Defaults to None.
            latitude (_type_, optional): The latitude for the geolocation of the end user. Defaults to None.
            longitude (_type_, optional): The longitude for the geolocation of the end user. Defaults to None.

        Returns:
            int: the index of the newly stored spam record.
        """
        user_id = self.__record_user_with_sql(
            connection=self.db_manager.connection,
            user_ip_address=user_ip_address,
            country_code=country_code,
            country_name=country_name,
            region=region,
            latitude=latitude,
            longitude=longitude,
        )

        spam_id = self.__record_spam_email_with_sql(
            connection=self.db_manager.connection, email=email, user_id=user_id
        )
        return spam_id

    def record_ham_email_with_sql(
        self,
        email: str,
        user_ip_address: str,
        country_code: str = None,
        country_name: str = None,
        region: str = None,
        latitude=None,
        longitude=None,
    ) -> int:
        """Store the email ain the SQL database.

        Args:
            email (str): the message to store.
            user_ip_address (str): the IP v4 ip address of the end user.
            country_code (str, optional): The country code for the geolocation of the end user. Defaults to None.
            country_name (str, optional): The country for the geolocation of the end user. Defaults to None.
            region (str, optional): The region for the geolocation of the end user. Defaults to None.
            latitude (_type_, optional): The latitude for the geolocation of the end user. Defaults to None.
            longitude (_type_, optional): The longitude for the geolocation of the end user. Defaults to None.

        Returns:
            int: the index of the newly stored email record.
        """
        user_id = self.__record_user_with_sql(
            connection=self.db_manager.connection,
            user_ip_address=user_ip_address,
            country_code=country_code,
            country_name=country_name,
            region=region,
            latitude=latitude,
            longitude=longitude,
        )

        spam_id = self.__record_ham_email_with_sql(
            connection=self.db_manager.connection, email=email, user_id=user_id
        )
        return spam_id

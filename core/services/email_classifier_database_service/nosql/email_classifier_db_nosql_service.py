"""Service for the CRUD operations with a Mongo database."""

import datetime

from core.services.email_classifier_database_service.email_classifier_db_service import (
    EmailClassifierDbService,
)


class EmailClassifierDbNoSqlService(EmailClassifierDbService):
    """Manage the Mongo database service.

    Args:
        EmailClassifierDbService (_type_): The abstract super class for the manager.
    """

    def __init__(self, **kwargs) -> None:
        """Instantiate the service."""
        super().__init__(**kwargs)

    def record_spam_email_with_nosql(
        self, email: str, user_ip_address: str
    ) -> int:
        """Store the email as a spam in the Mongo database.

        Args:
            email (str): the spam message to store.
            user_ip_address (str): the IP v4 ip address of the end user.

        Returns:
            int: the new index created
        """
        payload = {
            "email": email,
            "date-sent": datetime.datetime.now(tz=datetime.timezone.utc),
            "ip-address": user_ip_address,
            "comment": "",
        }
        l_payloads = self.db_manager.connection["email_scoring"]["spam_email"]

        # payload_id = l_payloads.insert_one(payload).inserted_id
        l_payloads.insert_one(payload)
        return 0  # payload_id

    def record_ham_email_with_nosql(
        self, email: str, user_ip_address: str
    ) -> int:
        """Store the email as a spam in the Mongo database.

        Args:
            email (str): the email message to store.
            user_ip_address (str): the IP v4 ip address of the end user.

        Returns:
            int: the new index created
        """
        payload = {
            "email": email,
            "date-sent": datetime.datetime.now(tz=datetime.timezone.utc),
            "ip-address": user_ip_address,
            "comment": "",
        }

        l_payloads = self.db_manager.connection.email_scoring.ham_email
        payload_id = l_payloads.insert_one(payload).inserted_id
        return payload_id

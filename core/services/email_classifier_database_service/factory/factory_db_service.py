"""Create an instance of type  database service manager.

Returns either a service manager for nosql mongoDB or pgsql db. 
"""

from core.services.email_classifier_database_service.email_classifier_db_service import (
    EmailClassifierDbService,
)
from core.services.email_classifier_database_service.nosql.email_classifier_db_nosql_service import (
    EmailClassifierDbNoSqlService,
)
from core.services.email_classifier_database_service.sql.email_classifier_db_sql_service import (
    EmailClassifierDbSqlService,
)
from core.utils.constants import NOSQL_MODE, SQL_MODE


class FactoryDbService:
    """Return an instance of db service through a factory pattern."""

    @staticmethod
    def new_instance_service_db(**kwargs) -> EmailClassifierDbService:
        """Return an instance of db manager.

        Args:
            **db_manager (core.utils.databases.managers.InterfaceDbManager): an instance of a db manager
        Returns:
            EmailClassifierDbService: an instance of database service manager
        """
        if SQL_MODE == kwargs.get("db_manager").mode:
            return EmailClassifierDbSqlService(**kwargs)
        elif NOSQL_MODE == kwargs.get("db_manager").mode:
            return EmailClassifierDbNoSqlService(**kwargs)

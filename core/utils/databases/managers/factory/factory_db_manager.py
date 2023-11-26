"""Create an instance of type  database manager.

Returns either a db manager for nosql mongoDB or pgsql db. 
"""

from core.utils.constants import NOSQL_MODE, SQL_MODE
from core.utils.databases.managers.interface_db_manager import (
    InterfaceDbManager,
)
from core.utils.databases.managers.nosql.mongo_db_manager import MongoDbManager
from core.utils.databases.managers.sql.postgres_db_manager import (
    PostgresDbManager,
)


class FactoryDbManager:
    """Return an instance of db manager through a factory pattern."""

    @staticmethod
    def new_instance_db_manager(**kwargs) -> InterfaceDbManager:
        """Return an instance of db manager.

        Args:
            **mode (core.utils.constants): NOSQL_MODE or SQL_MODE

        Returns:
            InterfaceDbManager: an instance of database manager.
        """
        if SQL_MODE == kwargs["mode"]:
            return PostgresDbManager(**kwargs)
        elif NOSQL_MODE == kwargs["mode"]:
            return MongoDbManager(**kwargs)

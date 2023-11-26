"""Define the cach redis manager class."""

from threading import Lock, Thread

import redis


class SingletonMeta(type):
    """Use for SingletonMeta class.

    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """Create an instance.

        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class RedisManager(metaclass=SingletonMeta):
    """Define the redis cache manager class.

    Args:
        metaclass (SingletonMeta, optional): The super class for singleton pattern. Defaults to SingletonMeta.
    """

    redis_cache: redis.Redis = None
    redis_connection_pool: redis.ConnectionPool = None

    def __init__(self, hostname: str = None, port: int = None) -> None:
        """Initialize the redis cache manager.

        Args:
            hostname (str, optional): The hostname for redis service. Defaults to None.
            port (int, optional): The port for redis service. Defaults to None.
        """
        if hostname is None or port is None:
            hostname = "192.168.0.14"
            port = 6379

        redis_connection_pool = redis.ConnectionPool(
            host=hostname, port=port, db=0
        )
        self.redis_cache = redis.StrictRedis(
            connection_pool=redis_connection_pool
        )

    def get_redis_cache(self):
        """Return the instance service for redis cache.

        Returns:
            Redis: the redis cache service instance.
        """
        return self.redis_cache

    def get_redis_connection_pool(self):
        """Get the redis cache connection pool.

        Returns:
            ConnectionPool: The connection pool for the redis cache service.
        """
        return self.redis_connection_pool

    def get_value(self, key: str):
        """Get a value from the cache according to the passed key.

        Args:
            key (str): The key to search in the cache.

        Returns:
            str: The value existing into cache or None
        """
        return self.redis_cache.get(name=key)

    def set_value(self, key: str, value: str):
        """Set a pair of key-value in the cache.

        Args:
            key (str): The key to store.
            value (str): The value to store associated to the key.

        Returns:
            ResponseT: Object responseT from redis api.
        """
        return self.redis_cache.set(name=key, value=value)

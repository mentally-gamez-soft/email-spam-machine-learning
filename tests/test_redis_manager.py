import unittest

from core import app_env
from core.utils.caches.redis_manager import RedisManager


class TestRedisManager(unittest.TestCase):
    def setUp(self) -> None:
        self.redis_manager = RedisManager(
            hostname=app_env["HOSTNAME"], port=app_env["REDIS_PORT"]
        )

    def test_redis_initialization(self):
        """Check the redis cache server is up."""

        self.assertIsNotNone(
            self.redis_manager.get_redis_cache, "The cache is not initialized."
        )
        self.assertIsNotNone(
            self.redis_manager.get_redis_connection_pool,
            "The connection pool is unknown !",
        )

    def test_set_and_get_value(self):
        """Check that it is possible to store a value in the cache and to get it back."""

        self.redis_manager.set_value(
            "182.35.21.0",
            "{'ip_address':'a','country_code':'s','country_name':'d','region':'e'}",
        )
        self.assertIsNotNone(
            self.redis_manager.get_value("182.35.21.0"),
            "The key does not exist in cache !",
        )

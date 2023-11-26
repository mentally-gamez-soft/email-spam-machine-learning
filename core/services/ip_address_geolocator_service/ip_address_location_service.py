"""An API to get the geographic location from an IP Address.

This class allows to identify where the end user is geographically located thanks to ip address
The API is checking the redis cache, the database and in last resort call an external webservice API
"""

import json

import country_converter as coco
import psycopg2
from ip2geotools.databases.noncommercial import DbIpCity

from core import app_env
from core.utils.caches.redis_manager import RedisManager
from core.utils.constants import SQL_MODE
from core.utils.databases.managers.factory.factory_db_manager import (
    FactoryDbManager,
)


class IpAddressLocationService:
    """Define the service for geolocation from an IP address."""

    def __init__(self, *args, **kwargs) -> None:
        """Initialize IpAddressLocationService wit the following arguments.

        Args:
            **ip_address (str): the ip address IPV4 of the end user
        """
        self.ip_address = kwargs.get("ip_address")
        self.response = {
            "ip_address": "",
            "country_code": "",
            "country_name": "",
            "region": "",
            "latitude": "",
            "longitude": "",
        }
        self.response["ip_address"] = self.ip_address

        self.hostname = app_env["HOSTNAME"]
        self.database = app_env["DB_NAME"]
        self.user = app_env["DB_USER"]
        self.password = app_env["DB_PASSWORD"]

    def is_known_ip_address(self) -> dict:
        """Indicate if the ip address of a end user has already call the service app.

        Returns:
            dict: {'status':(True,False), 'level':('cache','database','web-service','None')}
        """
        if self.__ip_address_exists_in_cache():
            return {"status": True, "level": "cache"}

        if self.__ip_address_exists_in_db():
            return {"status": True, "level": "database"}

        if self.__get_ip_address_from_webservice():
            return {"status": True, "level": "web-service"}

        return {"status": False, "level": "None"}

    def response(self) -> dict:
        """Get the self.response property of the instance.

        Returns:
            dict: self.response
        """
        return self.response

    def __ip_address_exists_in_cache(self) -> bool:
        return self.__get_ip_address_from_redis_cache()

    def __ip_address_exists_in_db(self) -> bool:
        return self.__get_ip_address_from_db()

    def __get_ip_address_from_webservice(self) -> bool:
        return self.__get_ip_address_from_ws_geotools()

    def __get_ip_address_from_redis_cache(self):
        redis_cache = RedisManager()
        cached_value = redis_cache.get_value(self.ip_address)

        if cached_value is not None:
            self.response = json.loads(cached_value.decode("utf-8"))
            return True

        return False

    def set_ip_address_in_redis_cache(self):
        """Set the geolocation for an ip address in the redis cache."""
        redis_cache = RedisManager()

        redis_cache.set_value(self.ip_address, json.dumps(self.response))

    def __get_ip_address_from_db(self) -> bool:
        ip_address_found = False
        if self.ip_address == "127.0.0.1":
            return ip_address_found

        try:
            postgres_db_manager = FactoryDbManager.new_instance_db_manager(
                mode=SQL_MODE,
                host=self.hostname,
                database=self.database,
                user=self.user,
                password=self.password,
            )
            postgres_db_manager.connect()

            sql_query = (
                'SELECT "COUNTRY_CODE", "COUNTRY_NAME", "REGION", "LATITUDE",'
                ' "LONGITUDE" FROM USERS WHERE "IP_ADDRESS_ORIGIN" = %s'
            )
            cursor = postgres_db_manager.connection.cursor()
            cursor.execute(sql_query, (self.ip_address,))
            records = cursor.fetchone()

            if records:
                for row in records:
                    ip_address_found = True
                    self.response["ip_address"] = self.ip_address
                    self.response["country_code"] = row[0]
                    self.response["country_name"] = row[1]
                    self.response["region"] = row[2]
                    self.response["latitude"] = row[3]
                    self.response["longitude"] = row[4]

            postgres_db_manager.disconnect()
        except (Exception, psycopg2.Error) as error:
            print("Error while fetching data from pgsql db", error)
        finally:
            cursor.close()
            postgres_db_manager.disconnect()

        return ip_address_found

    def __get_ip_address_from_ws_geotools(self) -> bool:
        res = DbIpCity.get(self.ip_address, api_key="free")

        if res.country:
            self.response["country_name"] = coco.convert(
                names=[
                    res.country,
                ],
                to="name_short",
            )
            self.response["country_code"] = res.country
        if res.region:
            self.response["region"] = res.region
        if res.latitude:
            self.response["latitude"] = res.latitude
        if res.longitude:
            self.response["longitude"] = res.longitude
        self.response["ip_address"] = self.ip_address

        if self.response.keys().__len__() > 1:
            return True

        return False

    # def __get_ip_address_from_ws_ipstack__(self) -> dict:
    #     params = ['query', 'status', 'country', 'countryCode', 'city', 'timezone', 'mobile','latitude','longitude','region_name']
    #     http_query = 'http://ip-api.com/json/{}'.format(self.ip_address)

    #     resp = requests.get(http_query, params={'fields': ','.join(params)})
    #     info = resp.json()

    #     return info

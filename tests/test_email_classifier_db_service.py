import unittest

from faker import Faker

from core import app_env
from core.services.email_classifier_database_service.factory.factory_db_service import (
    FactoryDbService,
)
from core.utils.constants import NOSQL_MODE, SQL_MODE
from core.utils.databases.managers.factory.factory_db_manager import (
    FactoryDbManager,
)


class TestEmailClassifierDbService(unittest.TestCase):
    def setUp(self) -> None:
        self.hostname = app_env["HOSTNAME"]
        self.database = app_env["DB_NAME"]
        self.user = app_env["DB_USER"]
        self.password = app_env["DB_PASSWORD"]

        self.postgres_db_manager = FactoryDbManager.new_instance_db_manager(
            mode=SQL_MODE,
            host=self.hostname,
            database=self.database,
            user=self.user,
            password=self.password,
        )

        # self.mongo_db_manager = FactoryDbManager.new_instance_db_manager(mode=NOSQL_MODE,
        #                                                                  host=self.hostname,
        #                                                                  database=self.database,
        #                                                                  user=self.user,
        #                                                                  password=self.password)

    def test_service_pgsql_is_initialized(self):
        """Test postgres database service is up and running."""

        pg_db_service = FactoryDbService.new_instance_service_db(
            db_manager=self.postgres_db_manager
        )
        self.assertTrue(
            pg_db_service.is_valid, "The database service is not accessible."
        )

    @unittest.skip("The nosql MongoDB source is not ready yet !!!!")
    def test_service_mongodb_is_initialized(self):
        """Test mongoDB database service is up and running."""

        mongo_db_service = FactoryDbService.new_instance_service_db(
            db_manager=self.mongo_db_manager
        )
        self.assertTrue(
            mongo_db_service.is_valid,
            "The database service is not accessible.",
        )

    def test_service_pgsql_is_sql_mode(self):
        """Test postgres database service is of type SQL."""

        pg_db_service = FactoryDbService.new_instance_service_db(
            db_manager=self.postgres_db_manager
        )
        self.assertEqual(
            pg_db_service.get_mode(),
            "SQL",
            "The database service is not of type sql.",
        )

    @unittest.skip("The nosql MongoDB source is not ready yet !!!!")
    def test_service_mongo_is_nosql_mode(self):
        """Test mongo database service is of type NOSQL."""

        mongo_db_service = FactoryDbService.new_instance_service_db(
            db_manager=self.mongo_db_manager
        )
        self.assertEqual(
            mongo_db_service.get_mode(),
            "NOSQL",
            "The database service is not of type sql.",
        )

    def test_service_pgsql_record_spam_email(self):
        """Test postgres database service CRUD store spam operation."""

        fixtures = self.__generate_fixtures(10)
        for fixture in fixtures:
            pg_db_service = FactoryDbService.new_instance_service_db(
                db_manager=self.postgres_db_manager
            )
            new_spam_id = pg_db_service.record_spam_email(
                ip_user=fixture, email=fixture["email"]
            )
            self.assertGreater(
                new_spam_id, 0, "The id for the recorded spam is incorrect"
            )

    @unittest.skip("The nosql MongoDB source is not ready yet !!!!")
    def test_service_mongo_record_spam_email(self):
        """Test mongo database service CRUD store spam operation."""

        user_ip = "160.20.3.65"
        email = (
            "Gift your business this Christmas by submitting your website to"
            " 10K+ directories on getlisted.directory."
        )
        mongo_db_service = FactoryDbService.new_instance_service_db(
            db_manager=self.mongo_db_manager
        )
        new_spam_id = mongo_db_service.record_spam_email(
            ip_user=user_ip, email=email
        )

        self.assertGreater(
            new_spam_id, 0, "The id for the recorded spam is incorrect"
        )

    def test_service_pgsql_record_ham_email(self):
        """Test postgres database service CRUD store email operation."""

        fixtures = self.__generate_fixtures(10)

        for fixture in fixtures:
            db_service = FactoryDbService.new_instance_service_db(
                db_manager=self.postgres_db_manager
            )
            new_ham_id = db_service.record_ham_email(
                ip_user=fixture, email=fixture["email"]
            )
            self.assertGreater(
                new_ham_id, 0, "The id for the recorded ham is incorrect"
            )

    def __generate_fixtures(self, nb_fixtures: int = 5) -> list:
        from faker.providers import address, internet, lorem

        fake = Faker(["fr_FR"])
        fake.add_provider(internet)
        fake.add_provider(address)
        fake.add_provider(lorem)
        test_fixtures = []

        for _ in range(nb_fixtures):
            elt = dict()
            elt["country_name"] = fake.country()
            elt["city"] = fake.city()
            elt["country_code"] = fake.country_code()
            elt["region"] = fake.postcode()
            elt["latitude"] = fake.latitude()
            elt["longitude"] = fake.longitude()
            elt["ip_address"] = fake.ipv4()
            elt["email"] = fake.paragraph(nb_sentences=6)
            test_fixtures.append(elt)
        return test_fixtures

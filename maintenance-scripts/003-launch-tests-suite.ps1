 & "./.venvpy311/Scripts/Activate.ps1"

python -m unittest tests/test_data_sanitizer.py
python -m unittest tests/test_email_classifier_db_service.py
python -m unittest tests/test_factory_db_manager.py
python -m unittest tests/test_factory_db_manager.py
python -m unittest tests/test_mongo_db_nosql_manager.py
python -m unittest tests/test_postgres_db_sql_manager.py
python -m unittest tests/test_redis_manager.py

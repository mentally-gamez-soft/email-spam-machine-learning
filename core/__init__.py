"""Configure the application with envs."""

from core.app_configuration.config import AppConfig, EnvLoader
from core.utils.constants import SQL_MODE

db_mode = SQL_MODE

# Expose Config object for app to import
env_loader = EnvLoader()
env_loader.get_env_config()
config = AppConfig(env_loader.env)
app_env = config.get_application_env()

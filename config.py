from pydantic import BaseSettings


class AppSettings(BaseSettings):
    """Configurable settings, got from environment"""

    # REDIS
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    # YAML FILE
    BUILDS_YAML_NAME: str = "test_builds"
    TASKS_YAML_NAME: str = "test_tasks"
    YAML_EXTENSION: str = "yaml"
    YAML_DIRECTORY: str = "builds"

    ROOT_DIRECTORY: str = "SaberInteractive"

    STATUS_OK: int = 1000


SETTINGS = AppSettings()

from fastapi import FastAPI

from config import SETTINGS
from app.handlers import tasks_router
from redis_staorage.connector import RedisConnector

from app.utils import load_builds, load_tasks

app = FastAPI()
app.include_router(tasks_router)

app.state.redis_connector = RedisConnector(
    host=SETTINGS.REDIS_HOST,
    port=SETTINGS.REDIS_PORT,
    db=SETTINGS.REDIS_DB,
)

app.state.redis_connector.put_dict(SETTINGS.BUILDS_YAML_NAME, load_builds())
app.state.redis_connector.put_dict(SETTINGS.TASKS_YAML_NAME, load_tasks())

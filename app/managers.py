from app.schemas import Build, GetTasksResponse

from app.utils import get_order_tasks
from app.errors import OperationError
from redis_storage.connector import RedisConnector
from config import SETTINGS


class Managers:
    @staticmethod
    def get_order_tasks(
        build: Build,
        connector: RedisConnector,
    ) -> GetTasksResponse:
        try:
            ordered_tasks: list[str] = get_order_tasks(
                build=build,
                connector=connector,
            )

            status = SETTINGS.STATUS_OK
            msg = {"ordered_tasks": ordered_tasks}
        except OperationError as error:
            status = error.status
            msg = error.msg

        response = {"status": status, "msg": msg}

        return GetTasksResponse(**response)

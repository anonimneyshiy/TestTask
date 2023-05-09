from fastapi import APIRouter, Depends

from app.managers import Managers
from app.schemas import Build, GetTasksResponse
from app.dependencies import get_redis_connector

tasks_router = APIRouter()


@tasks_router.post(
    "/tasks",
    response_model=GetTasksResponse,
)
async def get_tasks(
    build_info: Build,
    redis_connector=Depends(get_redis_connector)
) -> GetTasksResponse:
    response: GetTasksResponse = Managers.get_order_tasks(
        build=build_info,
        connector=redis_connector,
    )
    return response

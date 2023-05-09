from typing import Union

from pydantic import BaseModel


class Build(BaseModel):
    build: str


class Tasks(BaseModel):
    ordered_tasks: list[str]


class GetTasksResponse(BaseModel):
    status: int
    msg: Union[Tasks, str]

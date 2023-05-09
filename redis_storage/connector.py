from __future__ import annotations
from typing import Union, Any
import json

import redis


class RedisConnector:
    """ Connector for interactions with redis_storage """

    _db_instance: Union[redis.Redis, None] = None

    def __init__(
        self,
        host: str,
        port: int,
        db: int = 0,
    ) -> None:
        self._db_instance = redis.Redis(
            host=host,
            port=port,
            db=db,
        )

    def put_dict(
        self,
        key: str,
        value: Union[dict[str, list[str]], list[str]],
    ) -> None:
        print(key, value)
        json_value = json.dumps(value)
        self._db_instance.set(key, json_value)

    def get_dict(
        self,
        key: str
    ) -> dict[str, Any]:
        json_value = self._db_instance.get(key)
        result = json.loads(json_value)

        return result



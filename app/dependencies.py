from fastapi import Request

from redis_storage.connector import RedisConnector


async def get_redis_connector(request: Request) -> RedisConnector:
    return request.app.state.redis_connector

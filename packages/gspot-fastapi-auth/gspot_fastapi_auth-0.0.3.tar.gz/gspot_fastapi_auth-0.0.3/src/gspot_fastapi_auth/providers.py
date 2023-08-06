import redis.asyncio as redis

from .settings import token_config


class RedisClient:
    def __init__(self, host: str, port: int, db: int, password: str):
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.session = redis.Redis(
            host=self.host,
            port=self.port,
            db=self.db,
            password=self.password,
        )

    async def close(self):
        await self.session.close()


class RedisSingleton:
    _instance: RedisClient

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = RedisClient(token_config.host, token_config.port, token_config.db, token_config.password)
        return cls._instance

    @classmethod
    def init_redis(cls, host: str, port: int, db: int, password: str):
        cls._instance = RedisClient(host, port, db, password)


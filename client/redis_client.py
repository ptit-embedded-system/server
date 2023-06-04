import configparser
import redis


class RedisClient:
    _instance = None

    def __new__(cls, *args, **kwargs):
        config = configparser.ConfigParser()
        config.read('config/config.ini')

        host = config['redis']['host']
        port = int(config['redis']['port'])
        username = config['redis']['username']
        password = config['redis']['password']
        db = int(config['redis']['db'])
        if not cls._instance:
            cls._instance = super(RedisClient, cls).__new__(cls)
            cls._instance.redis_cli = redis.Redis(
                host=host,
                port=port,
                # username=username,
                # password=password,
                db=db
            )
        return cls._instance

    def set(self, key, value):
        self.redis_cli.set(key, value)

    def get(self, key) -> str:
        val = self.redis_cli.get(key)
        return val if val is not None else ""

    def keys(self) -> list[str]:
        key = self.redis_cli.keys("*")
        return [i.decode() for i in key]

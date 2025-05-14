from redis import Redis

from core.config import settings

redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)


def main():
    redis.set("hello", "hello")
    print(redis.keys())
    print(redis.get("hello"))


if __name__ == "__main__":
    main()

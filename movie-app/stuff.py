from redis import Redis

from core.config import settings

redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)


def main():
    redis.set("hello", "привет")
    print(redis.keys())
    print(redis.get("hello"))


if __name__ == "__main__":
    main()

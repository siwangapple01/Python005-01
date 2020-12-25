import redis
import os
from datetime import datetime

client = redis.Redis(host=os.getenv("NASIP"), port=6379, decode_responses=True)
client.flushdb()


def counter(video_id: int):
    client.incr(video_id)

    return client.get(video_id)


def main():
    print(counter(1001))
    print(counter(1002))
    print(counter(1001))
    print(counter(1002))


if __name__ == "__main__":
    main()


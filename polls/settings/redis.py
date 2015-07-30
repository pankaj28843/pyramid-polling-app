# Standard Library
import os


def get_redis_url():
    return os.environ["REDIS_URL"]

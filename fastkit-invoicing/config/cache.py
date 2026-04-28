import os

CACHE = {
    "DEFAULT": {
        "driver": os.getenv("CACHE_DRIVER", "redis"),
        "host": os.getenv("REDIS_HOST", "localhost"),
        "port": int(os.getenv("REDIS_PORT", 6379)),
        "db": int(os.getenv("REDIS_DB", 0)),
        "password": os.getenv("REDIS_PASSWORD", "your_password"),
        "ttl": int(os.getenv("CACHE_TTL", 300)),
    }
}

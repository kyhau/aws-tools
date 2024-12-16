from redis import Redis

ENDPOINT = "master.xxx.xxxxxx.apse2.cache.amazonaws.com"

redis = Redis(
    host=ENDPOINT,
    port=6379,
    decode_responses=True,
    ssl=True,
)

if redis.ping():
    print("Connected to Redis")

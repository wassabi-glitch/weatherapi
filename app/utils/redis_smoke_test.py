import redis
import os

# Fallback to local Redis if REDIS_URL is not set
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

r = redis.from_url(REDIS_URL, decode_responses=True)

# Write a value with a short TTL (expires in 30 seconds)
r.set("demo:greeting", "Hello Redis!", ex=30)

# Read it back
value = r.get("demo:greeting")
print("Read from Redis:", value)

# Optional: show TTL
ttl = r.ttl("demo:greeting")
print("Remaining TTL (seconds):", ttl)

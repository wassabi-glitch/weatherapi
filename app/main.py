import json
from fastapi import FastAPI
import redis
import os
import requests
import os
from fastapi import HTTPException
from datetime import date
from datetime import datetime, timedelta


app = FastAPI()

api_key = os.getenv("API_KEY")
base_url = os.getenv("BASE_URL")


# Connect to Redis
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
r = redis.from_url(REDIS_URL, decode_responses=True)
CACHE_TTL = 12 * 60 * 60


@app.get("/")
def home():
    return {"message": "Hello, Ahror! Your API works."}


@app.get("/weather")
def get_weather(city: str = "Tashkent", unit: str = "metric"):
    key = f"weather:{city.lower()}:{unit}"

    # 1) Try cache
    cached = r.get(key)
    if cached:
        return {"cache": "hit", "data": json.loads(cached)}

    # 2) Fetch from API
    url = f"{base_url}/{city}?unitGroup={unit}&key={api_key}"
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        return {"error": "Weather service unavailable", "status_code": response.status_code}
    data = response.json()

    # 3) Store in cache
    r.set(key, json.dumps(data), ex=CACHE_TTL)
    return {"cache": "miss", "data": data}


@app.get("/weather/daily")
def get_weather_for_date(city: str, unit: str, date: date):
    data = get_weather(city, unit)
    days = data["data"]["days"]

    for day in days:
        if day["datetime"] == date.isoformat():
            return {
                "date": day["datetime"],
                "mintemp": day["tempmin"],
                "maxtemp": day["tempmax"],
                "avgtemp": day["temp"],
                "description": day["description"]
            }
    raise HTTPException(status_code=404, detail="Date not found")


@app.get("/weather/hourly")
def get_weather_for_hour(city: str, unit: str, date: date, user_hour: str):
    # Parse user input into datetime.time
    try:
        user_time = datetime.strptime(user_hour, "%H:%M:%S")
    except ValueError:
        raise HTTPException(
            status_code=400, detail="Invalid time format, use HH:MM:SS")

    # Decide rounding rule → nearest hour
    hour = user_time.hour
    minutes = user_time.minute
    seconds = user_time.second

    if hour == 23 and (minutes >= 30 and seconds > 0):
        rounded_time = user_time.replace(hour=23, minute=0, second=0)

    elif minutes > 30 or (minutes == 30 and seconds > 0):
        # Round up
        rounded_time = user_time.replace(
            minute=0, second=0) + timedelta(hours=1)
    else:
        # Round down
        rounded_time = user_time.replace(minute=0, second=0)

    normalised_hour = rounded_time.strftime("%H:%M:%S")

    data = get_weather(city, unit)
    days = data["data"]["days"]

    for day in days:
        if day["datetime"] == date.isoformat():
            for h in day["hours"]:
                if h["datetime"] == normalised_hour:
                    return {
                        "requested": user_hour,
                        "matched": normalised_hour,
                        "time": h["datetime"],
                        "temperature": h["temp"],
                        "conditions": h["conditions"]
                    }
    raise HTTPException(status_code=404, detail="Hour not found")

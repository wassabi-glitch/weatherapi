

Client (frontend, mobile app, or another service)
   ↓
FastAPI route (/weather?city=Tashkent)
   ↓
Controller (handles request, validates input)
   ↓
Service (business logic: fetch weather data)
   ↓
Redis Cache (check if data already stored)
   ↓
External Weather API (only if cache miss)
   ↓
Redis Cache (store fresh data with TTL)
   ↓
Response (JSON back to client)


wsl -d Ubuntu
sudo service redis-server start
redis-cli ping
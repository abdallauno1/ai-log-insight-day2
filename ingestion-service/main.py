
import time, requests, os
from datetime import datetime

API_URL = os.getenv("API_URL", "http://api:8000")

logs = [
    {"timestamp": datetime.utcnow().isoformat(), "level": "INFO", "service": "order", "message": "Order created"},
    {"timestamp": datetime.utcnow().isoformat(), "level": "ERROR", "service": "payment", "message": "Timeout from gateway"},
    {"timestamp": datetime.utcnow().isoformat(), "level": "WARN", "service": "order", "message": "Retrying payment"}
]

time.sleep(5)
for log in logs:
    requests.post(f"{API_URL}/logs", json=log)

while True:
    time.sleep(60)

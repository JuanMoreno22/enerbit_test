import redis
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")
redis_client = redis.Redis.from_url(REDIS_URL)


def test_redis_connection(redis_client):
    try:
        # Intenta establecer y obtener una clave
        redis_client.set("test_connection", "success")
        test_value = redis_client.get("test_connection")
        print(f"Conexión a base de datos Redis - En linea: {test_value.decode('utf-8')}")  # Debería imprimir 'success'
    except Exception as e:
        print(f"Conexión a base de datos Redis - Error conexión:  {e}")
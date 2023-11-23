from fastapi import FastAPI
from app.config.database import engine, SessionLocal, test_postgresql_connection
from app.config.redis_client import redis_client, test_redis_connection

from alembic.config import Config
from alembic import command


from fastapi import FastAPI
from app.routers import CustomerRouter,workOrderRouter

app = FastAPI()



@app.on_event("startup")
async def startup_event():
    # Prueba la conexión a PostgreSQL
    test_postgresql_connection(engine)

    # Ejecutar migraciones de Alembic
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

    # Prueba la conexión a Redis
    test_redis_connection(redis_client)

app.include_router(CustomerRouter.customer_router)
app.include_router(workOrderRouter.work_order_router)


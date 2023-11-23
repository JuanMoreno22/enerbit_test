from sqlalchemy import create_engine,text

from sqlalchemy.orm import sessionmaker,declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


#Prueba de conexion a base de datos
def test_postgresql_connection(engine):
    try:
        # Intenta obtener una conexión y ejecutar una consulta simple
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print(f"Conexión a base de datos PostgreSQL - En linea: {result.scalar()}")  # Debería imprimir 1
    except Exception as e:
        print(f"Conexión a base de datos PostgreSQL - Error conexión {e}")

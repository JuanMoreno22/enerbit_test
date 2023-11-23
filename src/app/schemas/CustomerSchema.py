from pydantic import BaseModel,validator
from typing import Optional
from datetime import datetime
from uuid import UUID
import pytz
from datetime import datetime, timedelta

# Esquema para la creación de un cliente
class CustomerCreate(BaseModel):
    first_name: str
    last_name: str
    address: str

    # 'is_active' y 'created_at' son manejados por la lógica del backend por defecto.

# Esquema para la respuesta completa de un cliente,
class CustomerOut(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    address: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_active: bool
    created_at: datetime

    @validator('created_at', 'start_date', 'end_date', pre=True, always=True)
    def convert_utc_to_colombia(cls, value: datetime):
        if value is None:
            return None  # Retornar None si el valor es None
        timezone = pytz.timezone("America/Bogota")
        colombia_time = value.astimezone(timezone)
        return colombia_time.strftime("%Y-%m-%d %H:%M:%S")

    class Config:
        orm_mode = True  # Permite la conversión entre ORM y Pydantic

# Esquema para actualizar un cliente existente
class CustomerUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    address: Optional[str] = None



from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Optional
import enum

from ..schemas.CustomerSchema import CustomerOut 


# Enumerado para el estado de la orden de trabajo
class WorkOrderStatus(str, enum.Enum):
    new = 'new'
    done = 'done'
    cancelled = 'cancelled'

# Esquema para la creación de una orden de trabajo
class WorkOrderCreate(BaseModel):
    customer_id: UUID
    title: str
    planned_date_begin: datetime
    planned_date_end: datetime

# Esquema para la respuesta de una orden de trabajo
class WorkOrderOut(BaseModel):
    id: UUID
    customer_id: UUID
    title: str
    planned_date_begin: datetime
    planned_date_end: datetime
    status: WorkOrderStatus
    created_at: datetime

    class Config:
        orm_mode = True  # Permite la conversión entre ORM y Pydantic

# Esquema para actualizar una orden de trabajo
class WorkOrderUpdate(BaseModel):
    title: Optional[str] = None
    planned_date_begin: Optional[datetime] = None
    planned_date_end: Optional[datetime] = None
    status: Optional[WorkOrderStatus] = None


class WorkOrderWithCustomerOut(BaseModel):
    id: UUID
    title: str
    planned_date_begin: datetime
    planned_date_end: datetime
    status: str
    created_at: datetime
    customer: CustomerOut


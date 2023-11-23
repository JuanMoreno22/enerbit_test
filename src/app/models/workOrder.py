import uuid
from sqlalchemy import Column, String, Boolean, DateTime,ForeignKey,Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.config.database import Base


import enum



from datetime import datetime
import pytz
def get_colombia_time():
    timezone = pytz.timezone("America/Bogota")
    return datetime.now(timezone)


class WorkOrderStatus(enum.Enum):
    new = 'new'
    done = 'done'
    cancelled = 'cancelled'


class WorkOrder(Base):
    __tablename__ = "work_orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    customer_id = Column(UUID(as_uuid=True), ForeignKey('customers.id'), nullable=False)
    title = Column(String, nullable=False)
    planned_date_begin = Column(DateTime, nullable=False)
    planned_date_end = Column(DateTime, nullable=False)
    status = Column(Enum(WorkOrderStatus, name='work_order_status'), default=WorkOrderStatus.new, nullable=False)
    created_at = Column(DateTime, default=get_colombia_time, nullable=False)
    customer = relationship("Customer", back_populates="work_orders")



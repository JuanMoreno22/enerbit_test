from fastapi import APIRouter, Depends, HTTPException, status,Query
from datetime import datetime
from sqlalchemy.orm import Session
from typing import Optional, List

from ..schemas.workOrderSchema import WorkOrderCreate, WorkOrderOut, WorkOrderUpdate,WorkOrderWithCustomerOut
from ..helper.workOrderValidacions import validate_work_order_exists
from ..helper.custumerValidations import validate_customer_exists

from ..helper.validations import validate_dates,validate_date_order,validate_uuid,validate_datetime_format
from ..config.dependencies import get_db
from ..service.workOrder import (create_work_order, get_work_order_by_id,
                            update_work_order, delete_work_order,
                            get_all_work_orders, read_last_messages_from_redis_stream,
                            get_work_orders_service_filter,get_work_orders_by_customer_id)



work_order_router = APIRouter(tags=["workOrder"])

@work_order_router.post("/work_orders/", response_model=WorkOrderOut, status_code=status.HTTP_201_CREATED)
def create_work_order_endpoint(work_order: WorkOrderCreate, db: Session = Depends(get_db)):

    validate_datetime_format(work_order.planned_date_begin,"planned_date_begin")
    validate_datetime_format(work_order.planned_date_end,"planned_date_end")
    validate_date_order(work_order.planned_date_begin, work_order.planned_date_end)
    validate_dates(work_order.planned_date_begin, work_order.planned_date_end)
    return create_work_order(work_order, db)


@work_order_router.get("/work_orders/", response_model=List[WorkOrderWithCustomerOut])
def list_work_orders(db: Session = Depends(get_db)):
    return get_all_work_orders(db)

@work_order_router.get("/work_orders/filter/{work_order_id}", response_model=WorkOrderWithCustomerOut)
def read_work_order(work_order_id: str, db: Session = Depends(get_db)):
    validate_uuid(work_order_id)
    validate_work_order_exists(work_order_id, db)
    return get_work_order_by_id(work_order_id, db)

@work_order_router.get("/work-orders/customer/{customer_id}", response_model=List[WorkOrderWithCustomerOut])
def get_work_orders_by_customer_endpoint(customer_id: str, db: Session = Depends(get_db)):
    validate_uuid(customer_id)
    validate_customer_exists(customer_id, db)
    return get_work_orders_by_customer_id(db, customer_id)


@work_order_router.get("/work_orders/filter", response_model=List[WorkOrderWithCustomerOut])
def get_work_orders_filter(
    db: Session = Depends(get_db),
    since: Optional[datetime] = Query(None, alias="since"),
    until: Optional[datetime] = Query(None, alias="until"),
    status: Optional[str] = None
):
    return get_work_orders_service_filter(db, since, until, status)



@work_order_router.put("/work_orders/{work_order_id}", response_model=WorkOrderOut)
def update_work_order_endpoint(work_order_id: str, work_order: WorkOrderUpdate, db: Session = Depends(get_db)):

    validate_uuid(work_order_id)
    validate_work_order_exists(work_order_id, db)

    if(work_order.planned_date_begin and work_order.planned_date_end):
        validate_datetime_format(work_order.planned_date_begin,"planned_date_begin")
        validate_datetime_format(work_order.planned_date_end,"planned_date_end")
        validate_date_order(work_order.planned_date_begin, work_order.planned_date_end)
        # Se realiza la validacion de si la diferencia de fechas de pnanificación no supera 2 horas
        validate_dates(work_order.planned_date_begin, work_order.planned_date_end)

    return update_work_order(work_order_id, work_order, db)


@work_order_router.delete("/work_orders/{work_order_id}", response_model=WorkOrderOut)
def delete_work_order_endpoint(work_order_id: str, db: Session = Depends(get_db)):
    validate_uuid(work_order_id)
    validate_work_order_exists(work_order_id, db)
    return delete_work_order(work_order_id, db)


@work_order_router.get("/redis/work-order")
async def get_work_order_redis():
    # Aquí llamas a la función que lee los mensajes de Redis
    messages = read_last_messages_from_redis_stream('work_order_updates')
    return {"messages": messages}
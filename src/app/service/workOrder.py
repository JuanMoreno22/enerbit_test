from sqlalchemy.orm import Session,joinedload
from fastapi import HTTPException
from datetime import datetime
from ..models.workOrder import WorkOrder
from ..models.Customer import Customer
from ..schemas.workOrderSchema import WorkOrderCreate, WorkOrderUpdate
from ..config.redis_client import redis_client
from ..helper.formatter import get_colombia_time


from unidecode import unidecode


#----------------------------------------------------------------
def create_work_order(work_order_data: WorkOrderCreate, db: Session):
    try:
        new_work_order = WorkOrder(**work_order_data.model_dump())
        db.add(new_work_order)
        db.commit()
        db.refresh(new_work_order)
        return new_work_order
    except Exception as e:
        raise HTTPException(status_code=500, detail="Ocurrió un error al crear la orden de trabajo")

#----------------------------------------------------------------
def get_all_work_orders(db: Session):
    try:
        return db.query(WorkOrder).options(joinedload(WorkOrder.customer)).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Ocurrió un error al realizar la consulta")

#----------------------------------------------------------------
def get_work_order_by_id(work_order_id: str, db: Session):
    try:
        return  db.query(WorkOrder).options(joinedload(WorkOrder.customer)).filter(WorkOrder.id == work_order_id).first()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Ocurrió un error al realizar la consulta")

#----------------------------------------------------------------
def update_work_order(work_order_id: str, work_order_data: WorkOrderUpdate, db: Session):
    try:
        # Obtener la orden de trabajo
        work_order = db.query(WorkOrder).filter(WorkOrder.id == work_order_id).first()

        if work_order:
            # Actualizar los campos de la orden de trabajo
            for key, value in work_order_data.model_dump(exclude_unset=True).items():
                setattr(work_order, key, value)

            # Si 'title' no está en la actualización, usar el valor actual
            title_to_check = work_order_data.title if work_order_data.title is not None else work_order.title

            # Verificación para cambiar estado Costumer is_active = False
            formatted_title = unidecode(title_to_check.lower())
            if "suspension" in formatted_title or "cancelacion" in formatted_title:
                customer = db.query(Customer).filter(Customer.id == work_order.customer_id).first()
                if customer and customer.is_active:
                    customer.is_active = False
                    customer.end_date = get_colombia_time()   # Fecha y hora colombia
                    db.add(customer)

            # Verificar si el estado se cambió a "DONE"
            if work_order_data.status and work_order_data.status.lower() == "done":
                # Obtener el cliente asociado a la orden de trabajo
                customer = db.query(Customer).filter(Customer.id == work_order.customer_id).first()
                if customer and not customer.is_active:
                    # Contar las órdenes de trabajo completadas del cliente
                    completed_orders_count = db.query(WorkOrder).filter(
                        WorkOrder.customer_id == customer.id,
                        WorkOrder.status == "done"
                    ).count()

                    # Si esta es la primera orden completada, cambiar el estado del cliente
                    if completed_orders_count == 0:
                        customer.is_active = True
                        customer.start_date = get_colombia_time()  # Fecha y hora colombia
                        customer.end_date = None  # Resetear la end_date
                        db.add(customer)

                # Enviar el evento a Redis cuando se finaliza una orden
                event_data = {
                    'work_order_id': work_order_id,
                    'status': 'done',
                    'timestamp': get_colombia_time().isoformat()
                    # Puedes agregar más campos si es necesario
                }
                redis_client.xadd('work_order_updates', event_data)

            # Guardar los cambios en la base de datos
            db.commit()
            db.refresh(work_order)
            return work_order
    except Exception as e:
        raise HTTPException(status_code=500, detail="Ocurrió un error al realizar la consulta")



#----------------------------------------------------------------
# Consultar ultimos 10 mensajes almacenados en redis
def read_last_messages_from_redis_stream(stream_name, count=10):
    """
    Lee los últimos 'count' mensajes desde un stream de Redis.

    :param stream_name: El nombre del stream de Redis.
    :param count: Número de mensajes a leer, por defecto 10.
    :return: Lista de los últimos mensajes leídos desde el stream.
    """
    try:
        # Leer los últimos 'count' mensajes desde el stream
        stream_entries = redis_client.xrevrange(stream_name, count=count)

        # Procesar y devolver los mensajes
        messages = []
        for message_id, message in stream_entries:
            messages.append({'id': message_id, 'data': message})

        return messages

    except Exception as e:
        print(f"Error al leer desde el stream de Redis: {e}")
        raise HTTPException(status_code=500, detail="Ocurrió un error al realizar la consulta")


 #----------------------------------------------------------------
def delete_work_order(work_order_id: str, db: Session):
    try:
        work_order = db.query(WorkOrder).filter(WorkOrder.id == work_order_id).first()
        if work_order:
            db.delete(work_order)
            db.commit()
            return work_order
    except Exception as e:
            raise HTTPException(status_code=500, detail="Ocurrió un error al realizar la consulta")

#----------------------------------------------------------------
def get_work_orders_service_filter(db: Session, since: datetime, until: datetime, status: str):
    try:
        query = db.query(WorkOrder)

        if since:
            query = query.filter(WorkOrder.planned_date_begin >= since)
        if until:
            query = query.filter(WorkOrder.planned_date_end <= until)
        if status:
            query = query.filter(WorkOrder.status == status)

        # Agregar joinedload a la consulta ya filtrada
        query = query.options(joinedload(WorkOrder.customer))

        return query.all()
    except Exception as e:
            raise HTTPException(status_code=500, detail="Ocurrió un error al realizar la consulta")

#----------------------------------------------------------------
def get_work_orders_by_customer_id(db: Session, customer_id: str):
    try:
        # Realiza la consulta para obtener las órdenes de servicio del cliente
        return  db.query(WorkOrder).options(joinedload(WorkOrder.customer)).filter(WorkOrder.customer_id == customer_id).all()
    except Exception as e:
            raise HTTPException(status_code=500, detail="Ocurrió un error al realizar la consulta")

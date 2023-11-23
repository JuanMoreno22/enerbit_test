from datetime import datetime, timedelta
from fastapi import HTTPException
import uuid

def validate_dates(planned_date_begin: datetime, planned_date_end: datetime):
    if planned_date_end - planned_date_begin > timedelta(hours=2):
        raise HTTPException(status_code=400, detail="La duración entre las fechas supera las 2 horas")

def validate_date_order(fecha_begin: datetime, fecha_end: datetime):
    if fecha_end < fecha_begin:
        raise HTTPException(status_code=400, detail="La fecha de inicio no puede ser  mayor  a la fecha de finalización")



def validate_datetime_format(date_string: datetime, variable_name: str):
    if isinstance(date_string, str):
        try:
            datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Formato de fecha y hora incorrecto para '{variable_name}'. El formato correcto es yyyy-mm-dd hh:mm:ss")
    elif not isinstance(date_string, datetime):
        raise HTTPException(status_code=400, detail=f"El valor para '{variable_name}' debe ser una cadena de texto o un objeto datetime")

def validate_uuid(work_order_id: str):
    try:
        uuid_obj = uuid.UUID(work_order_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="El ID proporcionado no es un UUID válido")

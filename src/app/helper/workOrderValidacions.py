from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..models.workOrder import WorkOrder

def validate_work_order_exists(work_order_id: str, db: Session):
    work_order = db.query(WorkOrder).filter(WorkOrder.id == work_order_id).first()
    if not work_order:
        raise HTTPException(status_code=404, detail="Work_order no encontrado")

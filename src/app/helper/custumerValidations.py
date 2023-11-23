from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..models.Customer import Customer  # Asegúrate de importar tu modelo WorkOrder

def validate_customer_exists(customer_id: str, db: Session):
    customer= db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer no encontrado")

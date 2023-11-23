from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models.Customer import Customer
from ..schemas.CustomerSchema import CustomerCreate,CustomerUpdate
from app.helper.formatter import get_colombia_time


#----------------------------------------------------------------
def create_customer(customer_data: CustomerCreate, db: Session):
    try:
        # Obtiene la hora en "America/Bogota"
        colombia_time = get_colombia_time()
        # Agrega la hora a los datos del cliente antes de la inserción
        customer_data_dict = customer_data.dict()
        customer_data_dict['created_at'] = colombia_time
        new_customer = Customer(**customer_data_dict)
        db.add(new_customer)
        db.commit()
        db.refresh(new_customer)
        return new_customer
    except Exception as e:
            raise HTTPException(status_code=500, detail="Ocurrió un error al crear el registro")

#----------------------------------------------------------------
def get_all_customers(db: Session):
    try:
        return db.query(Customer).all()
    except Exception as e:
                raise HTTPException(status_code=500, detail="Ocurrió un error al realizar la consulta")

#----------------------------------------------------------------
def get_customer_by_id(customer_id: str, db: Session):
    try:
        return db.query(Customer).filter(Customer.id == customer_id).first()
    except Exception as e:
                raise HTTPException(status_code=500, detail="Ocurrió un error al realizar la consulta")

#----------------------------------------------------------------
def update_customer(customer_id: str, customer_data: CustomerUpdate, db: Session):
    try:
        customer = db.query(Customer).filter(Customer.id == customer_id).first()
        if customer:
            for key, value in customer_data.dict(exclude_unset=True).items():
                setattr(customer, key, value)
            db.commit()
            db.refresh(customer)
            return customer
    except Exception as e:
            raise HTTPException(status_code=500, detail="Ocurrió un error al realizar la consulta")

#----------------------------------------------------------------
def delete_customer(customer_id: str, db: Session):
    try:
        customer = db.query(Customer).filter(Customer.id == customer_id).first()
        if customer:
            db.delete(customer)
            db.commit()
            return customer
    except Exception as e:
                raise HTTPException(status_code=500, detail="Ocurrió un error al realizar la consulta")

#----------------------------------------------------------------
# Realiza la consulta para obtener los clientes activos
def get_active_customers(db: Session):
    try:
        return db.query(Customer).filter(Customer.is_active == True).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Ocurrió un error al realizar la consulta")
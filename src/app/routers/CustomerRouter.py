from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..schemas.CustomerSchema import CustomerCreate, CustomerOut, CustomerUpdate
from ..config.dependencies import get_db
from ..service.Customer import (create_customer, get_customer_by_id,
                                        update_customer, delete_customer, get_all_customers,get_active_customers)


from ..helper.custumerValidations import validate_customer_exists
from ..helper.validations import validate_uuid

customer_router = APIRouter(tags=["Customer"])

@customer_router.post("/customers/", response_model=CustomerOut, status_code=status.HTTP_201_CREATED)
def create_customer_endpoint(customer: CustomerCreate, db: Session = Depends(get_db)):
    return create_customer(customer, db)



@customer_router.get("/customers/", response_model=List[CustomerOut])
def list_customers(db: Session = Depends(get_db)):
    return get_all_customers(db)

@customer_router.get("/customers/{customer_id}", response_model=CustomerOut)
def read_customer(customer_id: str, db: Session = Depends(get_db)):
    validate_uuid(customer_id)
    validate_customer_exists(customer_id, db)
    return get_customer_by_id(customer_id, db)

@customer_router.get("/customers/all/active", response_model=List[CustomerOut])
def get_active_customers_endpoint(db: Session = Depends(get_db)):
    active_customers = get_active_customers(db)
    return active_customers

@customer_router.put("/customers/{customer_id}", response_model=CustomerOut)
def update_customer_endpoint(customer_id: str, customer: CustomerUpdate, db: Session = Depends(get_db)):
    validate_uuid(customer_id)
    validate_customer_exists(customer_id, db)
    return update_customer(customer_id, customer, db)

@customer_router.delete("/customers/{customer_id}", response_model=CustomerOut)
def delete_customer_endpoint(customer_id: str, db: Session = Depends(get_db)):
    validate_uuid(customer_id)
    validate_customer_exists(customer_id, db)
    return delete_customer(customer_id, db)




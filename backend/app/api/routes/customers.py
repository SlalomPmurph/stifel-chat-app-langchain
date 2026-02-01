from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from app.database.session import get_db
from app.services.customer_service import customer_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


# Pydantic schemas
class AccountResponse(BaseModel):
    id: int
    account_number: str
    account_type: str
    balance: float

    class Config:
        from_attributes = True


class CustomerResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str]
    account_status: str

    class Config:
        from_attributes = True


class CustomerDetailResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str]
    account_status: str
    accounts: List[AccountResponse]
    total_balance: float

    class Config:
        from_attributes = True


@router.get("", response_model=List[CustomerResponse])
async def get_customers(
    advisor_id: str = Query(..., description="Advisor ID"),
    db: Session = Depends(get_db)
):
    """
    Get all customers for an advisor
    """
    try:
        customers = customer_service.get_customers_by_advisor(db, advisor_id)
        return customers

    except Exception as e:
        logger.error(f"Error in get_customers: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{customer_id}", response_model=CustomerDetailResponse)
async def get_customer(
    customer_id: int,
    advisor_id: str = Query(..., description="Advisor ID"),
    db: Session = Depends(get_db)
):
    """
    Get detailed customer information including accounts
    """
    try:
        # Get customer with access check
        customer = customer_service.get_customer_by_id(db, customer_id, advisor_id)

        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")

        # Get accounts
        accounts = customer_service.get_customer_accounts(db, customer_id)

        # Calculate total balance
        total_balance = customer_service.get_total_balance(db, customer_id)

        return CustomerDetailResponse(
            id=customer.id,
            name=customer.name,
            email=customer.email,
            phone=customer.phone,
            account_status=customer.account_status,
            accounts=[
                AccountResponse(
                    id=acc.id,
                    account_number=acc.account_number,
                    account_type=acc.account_type,
                    balance=acc.balance
                )
                for acc in accounts
            ],
            total_balance=total_balance
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_customer: {e}")
        raise HTTPException(status_code=500, detail=str(e))


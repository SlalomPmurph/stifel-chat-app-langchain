from sqlalchemy.orm import Session
from app.models.customer import Customer, Account
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


class CustomerService:
    """Service for customer-related operations"""

    @staticmethod
    def get_customers_by_advisor(db: Session, advisor_id: str) -> List[Customer]:
        """Get all customers for a specific advisor"""
        try:
            customers = db.query(Customer).filter(
                Customer.advisor_id == advisor_id
            ).all()
            return customers
        except Exception as e:
            logger.error(f"Error fetching customers: {e}")
            raise

    @staticmethod
    def get_customer_by_id(db: Session, customer_id: int, advisor_id: str) -> Optional[Customer]:
        """Get a specific customer by ID (with advisor access check)"""
        try:
            customer = db.query(Customer).filter(
                Customer.id == customer_id,
                Customer.advisor_id == advisor_id
            ).first()
            return customer
        except Exception as e:
            logger.error(f"Error fetching customer: {e}")
            raise

    @staticmethod
    def create_customer(db: Session, advisor_id: str, name: str, email: str, phone: str = None) -> Customer:
        """Create a new customer"""
        try:
            customer = Customer(
                advisor_id=advisor_id,
                name=name,
                email=email,
                phone=phone
            )
            db.add(customer)
            db.commit()
            db.refresh(customer)
            return customer
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating customer: {e}")
            raise

    @staticmethod
    def get_customer_accounts(db: Session, customer_id: int) -> List[Account]:
        """Get all accounts for a customer"""
        try:
            accounts = db.query(Account).filter(
                Account.customer_id == customer_id
            ).all()
            return accounts
        except Exception as e:
            logger.error(f"Error fetching accounts: {e}")
            raise

    @staticmethod
    def get_total_balance(db: Session, customer_id: int) -> float:
        """Calculate total balance across all accounts for a customer"""
        try:
            accounts = db.query(Account).filter(
                Account.customer_id == customer_id
            ).all()
            return sum(account.balance for account in accounts)
        except Exception as e:
            logger.error(f"Error calculating total balance: {e}")
            raise


customer_service = CustomerService()


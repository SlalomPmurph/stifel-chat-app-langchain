"""
Seed the database with sample data for testing
"""
from app.database.session import SessionLocal, init_db
from app.models.customer import Customer, Account
import random


def seed_database():
    """Seed database with sample customers and accounts"""

    # Initialize database
    init_db()

    db = SessionLocal()

    try:
        # Check if data already exists
        existing_customers = db.query(Customer).count()
        if existing_customers > 0:
            print(f"Database already has {existing_customers} customers. Skipping seed.")
            return

        # Sample customer data
        customers_data = [
            {
                "advisor_id": "advisor-1",
                "name": "John Smith",
                "email": "john.smith@email.com",
                "phone": "555-0101"
            },
            {
                "advisor_id": "advisor-1",
                "name": "Sarah Johnson",
                "email": "sarah.johnson@email.com",
                "phone": "555-0102"
            },
            {
                "advisor_id": "advisor-1",
                "name": "Michael Brown",
                "email": "michael.brown@email.com",
                "phone": "555-0103"
            },
            {
                "advisor_id": "advisor-1",
                "name": "Emily Davis",
                "email": "emily.davis@email.com",
                "phone": "555-0104"
            },
            {
                "advisor_id": "advisor-1",
                "name": "Robert Wilson",
                "email": "robert.wilson@email.com",
                "phone": "555-0105"
            },
        ]

        # Account types and balance ranges
        account_types = ["checking", "savings", "investment", "retirement"]

        # Create customers and accounts
        for customer_data in customers_data:
            # Create customer
            customer = Customer(**customer_data)
            db.add(customer)
            db.flush()  # Flush to get the customer ID

            # Create 2-4 accounts for each customer
            num_accounts = random.randint(2, 4)
            for i in range(num_accounts):
                account_type = account_types[i % len(account_types)]

                # Generate realistic balances
                if account_type == "checking":
                    balance = round(random.uniform(1000, 25000), 2)
                elif account_type == "savings":
                    balance = round(random.uniform(10000, 75000), 2)
                elif account_type == "investment":
                    balance = round(random.uniform(50000, 500000), 2)
                else:  # retirement
                    balance = round(random.uniform(100000, 1000000), 2)

                account = Account(
                    customer_id=customer.id,
                    account_number=f"ACC-{customer.id:04d}-{i+1:02d}",
                    account_type=account_type,
                    balance=balance
                )
                db.add(account)

        # Commit all changes
        db.commit()
        print("✅ Database seeded successfully!")
        print(f"   Created {len(customers_data)} customers")
        print(f"   Created multiple accounts per customer")

    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()


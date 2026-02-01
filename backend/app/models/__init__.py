"""Empty __init__.py to make models a package"""

# Import all models here for easier access
from app.models.customer import Customer, Account
from app.models.chat import ChatSession, ChatMessage

__all__ = ["Customer", "Account", "ChatSession", "ChatMessage"]


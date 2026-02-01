from sqlalchemy.orm import Session
from app.models.chat import ChatSession, ChatMessage
from typing import List, Optional
import uuid
import logging

logger = logging.getLogger(__name__)


class ChatService:
    """Service for chat session and message operations"""

    @staticmethod
    def create_session(db: Session, advisor_id: str) -> ChatSession:
        """Create a new chat session"""
        try:
            session_id = str(uuid.uuid4())
            session = ChatSession(
                session_id=session_id,
                advisor_id=advisor_id
            )
            db.add(session)
            db.commit()
            db.refresh(session)
            return session
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating chat session: {e}")
            raise

    @staticmethod
    def get_session(db: Session, session_id: str, advisor_id: str) -> Optional[ChatSession]:
        """Get a chat session by ID (with advisor access check)"""
        try:
            session = db.query(ChatSession).filter(
                ChatSession.session_id == session_id,
                ChatSession.advisor_id == advisor_id
            ).first()
            return session
        except Exception as e:
            logger.error(f"Error fetching chat session: {e}")
            raise

    @staticmethod
    def add_message(
        db: Session,
        session_id: int,
        role: str,
        content: str,
        chart_data: dict = None
    ) -> ChatMessage:
        """Add a message to a chat session"""
        try:
            message = ChatMessage(
                session_id=session_id,
                role=role,
                content=content,
                chart_data=chart_data
            )
            db.add(message)
            db.commit()
            db.refresh(message)
            return message
        except Exception as e:
            db.rollback()
            logger.error(f"Error adding chat message: {e}")
            raise

    @staticmethod
    def get_session_messages(db: Session, session_id: int) -> List[ChatMessage]:
        """Get all messages for a chat session"""
        try:
            messages = db.query(ChatMessage).filter(
                ChatMessage.session_id == session_id
            ).order_by(ChatMessage.timestamp).all()
            return messages
        except Exception as e:
            logger.error(f"Error fetching chat messages: {e}")
            raise


chat_service = ChatService()


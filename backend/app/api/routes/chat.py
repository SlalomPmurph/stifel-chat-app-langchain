from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from app.database.session import get_db
from app.services.chat_service import chat_service
from app.services.langchain_service import langchain_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


# Pydantic schemas
class ChatMessageRequest(BaseModel):
    message: str
    advisor_id: str
    session_id: Optional[str] = None


class ChatMessageResponse(BaseModel):
    response: str
    session_id: str
    chart_data: Optional[dict] = None


class CreateSessionRequest(BaseModel):
    advisor_id: str


class CreateSessionResponse(BaseModel):
    session_id: str
    advisor_id: str


@router.post("/message", response_model=ChatMessageResponse)
async def send_message(
    request: ChatMessageRequest,
    db: Session = Depends(get_db)
):
    """
    Send a chat message and get AI response
    """
    try:
        # Get or create session
        session = None
        if request.session_id:
            session = chat_service.get_session(db, request.session_id, request.advisor_id)

        if not session:
            # Create new session if none exists
            session = chat_service.create_session(db, request.advisor_id)

        # Save user message
        chat_service.add_message(
            db=db,
            session_id=session.id,
            role="user",
            content=request.message
        )

        # Get AI response using LangChain
        ai_response = await langchain_service.chat(
            message=request.message,
            advisor_id=request.advisor_id,
            session_id=session.session_id
        )

        # Save assistant message
        chat_service.add_message(
            db=db,
            session_id=session.id,
            role="assistant",
            content=ai_response["response"],
            chart_data=ai_response.get("chart_data")
        )

        return ChatMessageResponse(
            response=ai_response["response"],
            session_id=session.session_id,
            chart_data=ai_response.get("chart_data")
        )

    except Exception as e:
        logger.error(f"Error in send_message: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/session", response_model=CreateSessionResponse)
async def create_session(
    request: CreateSessionRequest,
    db: Session = Depends(get_db)
):
    """
    Create a new chat session
    """
    try:
        session = chat_service.create_session(db, request.advisor_id)

        return CreateSessionResponse(
            session_id=session.session_id,
            advisor_id=session.advisor_id
        )

    except Exception as e:
        logger.error(f"Error in create_session: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history/{session_id}")
async def get_chat_history(
    session_id: str,
    advisor_id: str,
    db: Session = Depends(get_db)
):
    """
    Get chat history for a session
    """
    try:
        # Get session with access check
        session = chat_service.get_session(db, session_id, advisor_id)

        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        # Get messages
        messages = chat_service.get_session_messages(db, session.id)

        return {
            "session_id": session.session_id,
            "messages": [
                {
                    "id": msg.id,
                    "role": msg.role,
                    "content": msg.content,
                    "chart_data": msg.chart_data,
                    "timestamp": msg.timestamp.isoformat()
                }
                for msg in messages
            ]
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_chat_history: {e}")
        raise HTTPException(status_code=500, detail=str(e))


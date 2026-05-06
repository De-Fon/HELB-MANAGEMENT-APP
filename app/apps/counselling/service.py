from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.apps.counselling.repository import CounsellingRepository
from app.apps.counselling.schemas import CounsellingBookingCreate
from app.apps.counselling.models import CounsellingSession

class CounsellingService:
    def __init__(
        self, 
        repository: CounsellingRepository,
        idempotency_service=None
    ):
        self.repository = repository
        self.idempotency_service = idempotency_service
    def book_session(self, db: Session, data: CounsellingBookingCreate) -> CounsellingSession:
        allowed_types = ["money_management", "relationship_advice"]
        
        if data.session_type not in allowed_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid session type. Must be one of: {', '.join(allowed_types)}"
            )

        booking = self.repository.create_booking(db, data)
        db.commit()
        return booking

from sqlalchemy.orm import Session
from app.apps.counselling.models import CounsellingSession
from app.apps.counselling.schemas import CounsellingBookingCreate

class CounsellingRepository:
    def create_booking(self, db: Session, data: CounsellingBookingCreate) -> CounsellingSession:
        db_session = CounsellingSession(**data.model_dump())
        db.add(db_session)
        db.flush()
        db.refresh(db_session)
        return db_session

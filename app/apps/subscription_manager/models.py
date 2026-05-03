from sqlalchemy import Column, Integer, String, Float, Boolean, Date
from app.core.database import Base

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    service_name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    renewal_date = Column(Date, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    auto_renew = Column(Boolean, default=True, nullable=False)

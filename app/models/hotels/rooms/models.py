from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB

from app.database import Base


class Rooms(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    service = Column(JSONB, nullable=False)
    quantity = Column(Integer, nullable=False)
    image_id = Column(Integer, nullable=False)

from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import JSONB

from app.database import Base


class Hotels(Base):
    __tablename__ = "hotels"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    service = Column(JSONB, nullable=False)
    rooms_quantity = Column(Integer, nullable=False)
    image_id = Column(Integer)

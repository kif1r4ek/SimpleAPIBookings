from sqlalchemy import Column, Computed, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.database import Base


class Bookings(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    date_from = Column(DateTime, nullable=False)
    date_to = Column(DateTime, nullable=False)
    price = Column(Integer, nullable=False)

    # разница в днях = секунды/86400, приводим к int
    total_days = Column(
        Integer,
        Computed("(EXTRACT(EPOCH FROM (date_to - date_from)) / 86400)::int"),
        nullable=False,
    )

    # целые дни * цена -> int
    total_cost = Column(
        Integer,
        Computed("((EXTRACT(EPOCH FROM (date_to - date_from)) / 86400)::int * price)"),
        nullable=False,
    )

    user = relationship("Users", back_populates="bookings")

    def __str__(self):
        return f"Booking(id={self.id})"

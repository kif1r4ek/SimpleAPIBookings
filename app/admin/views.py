from sqladmin import ModelView

from app.models.bookings.models import Bookings
from app.models.users.models import Users


class UsersAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.email]
    can_delete = False
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"
    column_details_exclude_list = [Users.password]


class BookingsAdmin(ModelView, model=Bookings):
    column_list = [columns.name for columns in Bookings.__table__.columns] + [Bookings.user]
    name = "Бронь"
    name_plural = "Брони"

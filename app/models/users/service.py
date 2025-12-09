from app.models.users.models import Users
from app.service.base import BaseService


class UsersService(BaseService):
    model = Users

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users.service import UsersService


@pytest.mark.parametrize("user_id, exists", [
    (1, True),
    (2, True),
    (5, False),
    (6, False),
])
async def test_user_find_by_id(session: AsyncSession, user_id, exists) -> None:
    user = await UsersService.find_by_id(session,user_id)

    if exists:
        assert user
        assert user.id == user_id
    else:
        assert not user



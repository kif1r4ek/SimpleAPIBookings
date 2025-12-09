import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("email,password,staus_code", [
    ("kot@pes.com", "cotopes", 200),
    ("kot@pes.com", "cot9pes", 409),
    ("pes@pes.com", "pespes", 200),
    ("dsfdf", "pespes", 422),
])
async def test_register_user(email,password, staus_code, async_client: AsyncClient) -> None:
    response = await async_client.post("/auth/register",
                                       json={"email": email, "password": password})
    assert response.status_code == staus_code


@pytest.mark.parametrize("email,password,staus_code", [
    ("fedor@moloko.ru", "tut_budet_hashed_password_1", 200),
    ("sharik@moloko.ru", "tut_budet_hashed_password_2", 200),
    ("kot@pes.com", "cotopes", 200),
])
async def test_login_user(email,password, staus_code, async_client: AsyncClient) -> None:
    response = await async_client.post("/auth/login",
                                       json={"email": email, "password": password})
    assert response.status_code == staus_code
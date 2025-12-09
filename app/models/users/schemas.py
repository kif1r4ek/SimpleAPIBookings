from pydantic import BaseModel, ConfigDict, EmailStr


class SUserAuth(BaseModel):
    email: EmailStr
    password: str

    model_config = ConfigDict(from_attributes=True)

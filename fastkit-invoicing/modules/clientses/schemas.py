from pydantic import Field, EmailStr
from fastkit_core.validation import (
    BaseSchema,
    BaseCreateSchema,
    BaseUpdateSchema
)
from app.models.enums import Languages


class ClientsCreate(BaseCreateSchema):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = Field(None, max_length=255)
    language: Languages = Field(default=Languages.EN)

    email: EmailStr | None = None
    phone: str | None = Field(None, max_length=50)

    address: str | None = Field(None, max_length=500)
    city: str | None = Field(None, max_length=100)
    country: str | None = Field(None, max_length=100)
    postal_code: str | None = Field(None, max_length=20)


class ClientsUpdate(BaseUpdateSchema):
    name: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = Field(None, max_length=255)
    language: Languages | None = None
    email: EmailStr | None = None
    phone: str | None = Field(None, max_length=50)
    address: str | None = Field(None, max_length=500)
    city: str | None = Field(None, max_length=100)
    country: str | None = Field(None, max_length=100)
    postal_code: str | None = Field(None, max_length=20)


class ClientsResponse(BaseSchema):
    id: int
    name: str
    description: str | None
    email: str | None
    phone: str | None
    address: str | None
    city: str | None
    country: str | None
    postal_code: str | None

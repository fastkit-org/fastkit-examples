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
    description: str | None = None
    email: str | None = None
    phone: str | None = None
    address: str | None = None
    city: str | None = None
    country: str | None = None
    postal_code: str | None = None

    model_config = {"from_attributes": True}


# Alias za konzistentnost sa relacijama (Invoice koristi ClientResponse)
ClientResponse = ClientsResponse

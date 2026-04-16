from typing import TYPE_CHECKING
from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from fastkit_core.database import BaseWithTimestamps, SoftDeleteMixin, IntIdMixin
from app.models.enums import Languages

if TYPE_CHECKING:
    from app.models.invoice import Invoice

class Client(IntIdMixin, BaseWithTimestamps, SoftDeleteMixin):
    __tablename__ = "clients"

    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] =  mapped_column(String(255))
    language: Mapped[Languages] = mapped_column(
        Enum(Languages, name="language"),
        default=Languages.EN,
        nullable=False
    )

    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    address: Mapped[str | None] = mapped_column(String(500), nullable=True)
    city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    country: Mapped[str | None] = mapped_column(String(100), nullable=True)
    postal_code: Mapped[str | None] = mapped_column(String(20), nullable=True)

    invoices: Mapped[list["Invoice"]] = relationship(back_populates="client")

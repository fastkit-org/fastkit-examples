import enum

class Languages(str, enum.Enum):
    EN = "en"
    DE = "de"
    ES = "es"

class InvoicesStatus(str, enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    CANCELED = "canceled"
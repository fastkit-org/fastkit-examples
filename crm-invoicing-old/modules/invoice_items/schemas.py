from fastkit_core.validation import BaseSchema
from pydantic import Field, model_validator, computed_field
from typing import Optional

class InvoiceItemCreate(BaseSchema):
    product_id: int = Field(gt=0, description="Product ID")
    quantity: int = Field(default=1, ge=1, description="Quantity (min: 1)")
    unit_price: float =  Field(gt=0, description="Unit Price")

class InvoiceItemUpdate(BaseSchema):
    quantity: int | None = Field(None, ge=1)
    unit_price: float | None = Field(None, gt=0)

class InvoiceItemResponse(BaseSchema):
    quantity: int
    unit_price: float

    product_name: Optional[str] = None
    product_sku: Optional[str] = None
    product_slug: Optional[str] = None
    product_description: Optional[str] = None

    model_config = {"from_attributes": True}

    @model_validator(mode='before')
    @classmethod
    def extract_product_data(cls, data):
        product = getattr(data, 'product', None)

        if product:
            data.product_name = product.name
            data.product_sku = product.sku
            data.product_slug = product.slug
            data.product_description = product.description

        return data

    @computed_field
    @property
    def total(self) -> float:
        return self.quantity * self.unit_price

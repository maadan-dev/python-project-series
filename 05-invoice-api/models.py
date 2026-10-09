from pydantic import BaseModel, Field

class LineItem(BaseModel):
    description: str = Field(
        title="The description of the item",
        min_length=1
    )
    quantity: int = Field(
        ge=1,
        description="Enter the quantity"
    )
    unit_price: float = Field(
        gt=0,
        description="Enter the unit price"
    )

class Invoice(BaseModel):
    client_name: str = Field(
        description="Client name",
        min_length=1
    )
    items: list[LineItem] = Field(
        min_length=1,
        description="Items"
    )

class InvoiceOut(Invoice):
    id: int
    created_at: str
    status: str
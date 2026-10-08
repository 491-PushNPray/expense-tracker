from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TransactionType(str, Enum):
    income = "income"
    expense = "expense"


class CategoryInput(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    type: TransactionType
    is_default: bool = False

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("Name cannot be empty")
        return normalized


class CategoryCreate(CategoryInput):
    pass


class CategoryUpdate(CategoryInput):
    pass


class Category(CategoryInput):
    id: str


class TransactionInput(BaseModel):
    amount: float = Field(gt=0, allow_inf_nan=False)
    type: TransactionType
    date: date
    description: str | None = Field(default=None, max_length=500)
    category_id: str = Field(min_length=1)

    @field_validator("description")
    @classmethod
    def normalize_description(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip()
        return normalized or None


class TransactionCreate(TransactionInput):
    pass


class TransactionUpdate(TransactionInput):
    pass


class Transaction(TransactionInput):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

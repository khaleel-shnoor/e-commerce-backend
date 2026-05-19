"""Shared Pydantic schemas."""

from pydantic import BaseModel, ConfigDict


class SchemaBase(BaseModel):
    """Base schema with ORM mode for SQLAlchemy model conversion."""

    model_config = ConfigDict(from_attributes=True)


class MessageResponse(SchemaBase):
    message: str

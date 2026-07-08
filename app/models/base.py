"""Shared SQLAlchemy base classes for all application models."""

import uuid, enum
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import as_declarative, declared_attr


@as_declarative()
class BaseEntity:
    """Provide shared identifiers and timestamps for persisted entities."""

    # Unique identifier for the entity
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # Timestamp indicating when the record was first created.
    created_at = Column(DateTime, default=datetime.now(tz=timezone.utc), nullable=False)
    # Timestamp indicating when the record was last updated.
    updated_at = Column(DateTime, default=datetime.now(tz=timezone.utc), onupdate=datetime.now(tz=timezone.utc), nullable=False)

    @declared_attr
    def __tablename__(cls) -> str:
        """Generate a table name automatically from the class name."""
        return cls.__name__.lower() + "s"
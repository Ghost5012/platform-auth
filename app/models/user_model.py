
from app.models.base import BaseEntity
from sqlalchemy import Column, String, Boolean


class User(BaseEntity):
    __tablename__ = "users"
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    role = Column(String, nullable=True)  # Role can be a string representing the user's role
    
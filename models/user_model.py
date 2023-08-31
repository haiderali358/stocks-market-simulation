from sqlalchemy import Column, String, Float

from models.base_model import BaseModel


class User(BaseModel):
    __tablename__ = "user"
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String(120), unique=True, nullable=False)
    balance = Column(Float(30), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

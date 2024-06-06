from sqlalchemy import Column, Integer, String, Float, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)


class Contract(Base):
    __tablename__ = 'contract'
    id = Column(Integer, primary_key=True)
    description = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User', backref='Contracts') # Not implemented foreign key and cascades
    created_at = Column(DateTime, default=func.now())
    fidelity = Column(Integer)
    amount = Column(Float())

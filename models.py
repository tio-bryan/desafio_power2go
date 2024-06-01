from sqlalchemy import Column, Integer, String, Float, DateTime, func, ForeignKey
from sqlalchemy.orm import backref, relationship
from database import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)


class Contract(Base):
    __tablename__ = "contract"
    id = Column(Integer, primary_key=True)
    description = Column(String)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship(
        User, backref=backref("contracts", uselist=True, cascade="delete,all")
    )
    created_at = Column(DateTime, default=func.now())
    fidelity = Column(Integer)
    amount = Column(Float())

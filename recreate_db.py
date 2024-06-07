from database import Base, engine
from models import User, Contract


_user = User
_contract = Contract
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

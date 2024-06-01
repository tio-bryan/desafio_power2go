from database import Base, engine, db_session
from models import User, Contract


Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

bryan = User(
    name='Bryan',
    email='bryan@gmail.com'
)
db_session.add(bryan)

munekata = User(
    name='Munekata',
    email='munekata@gmail.com'
)
db_session.add(munekata)

contract_1 = Contract(
    description='Contract 1',
    user=bryan,
    fidelity=53,
    amount=43
)
db_session.add(contract_1)

contract_2 = Contract(
    description='Contract 2',
    user=munekata,
    fidelity=88,
    amount=99
)
db_session.add(contract_2)

db_session.commit()

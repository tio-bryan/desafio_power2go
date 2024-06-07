from database import db_session
from models import User, Contract


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

contract = Contract(
        description='Contract 1',
        user=bryan,
        fidelity=53,
        amount=43
    )
db_session.add(contract)

contract = Contract(
        description='Contract 2',
        user=bryan,
        fidelity=53,
        amount=43
    )
db_session.add(contract)

for i in range(3, 10):
    contract = Contract(
        description='Contract ' + str(i),
        user=munekata,
        fidelity=53,
        amount=43
    )
    db_session.add(contract)


db_session.commit()

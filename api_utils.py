from graphql import GraphQLError

from database import db_session


def get_by_id(model, id):
    query = db_session.query(model).filter_by(id=id)

    if query.count() == 0:
        raise GraphQLError(model.__name__ + ' not found')

    return query.first()


def get_contracts_by_user_id(model, id):
    query = db_session.query(model).filter_by(user_id=id)

    if query.count():
        raise GraphQLError('User not deleted. User has linked contracts.')


def create(model):
    db_session.add(model)
    db_session.commit()

    return model


def update(model, id, input):
    query = db_session.query(model).filter_by(id=id)

    if query.count() == 0:
        raise GraphQLError(model.__name__ + ' not found')

    query.update(input)
    db_session.commit()

    return query.first()


def delete(model, id):
    query = db_session.query(model).filter_by(id=id)

    if query.count() == 0:
        return {'success': False, 'message': model.__name__ + ' not found'}

    query.delete()
    db_session.commit()

    return {'success': True, 'message': 'Deleted'}

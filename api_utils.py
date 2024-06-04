from database import db_session


def create(model):
    db_session.add(model)
    db_session.commit()

    return model


def update(model, id, input):
    db_session.query(model).filter_by(id=id).update(input)
    db_session.commit()

    return db_session.query(model).filter_by(id=id).first()


def delete(model, id):
    get = db_session.query(model).filter_by(id=id)

    if get.count() == 0:
        return {'success': False, 'message': model.__name__ + ' not found'}

    get.delete()
    db_session.commit()

    return {'success': True, 'message': 'Deleted'}

import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType

from models import User as UserModel
from models import Contract as ContractModel


class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        interfaces = (relay.Node,)


class Contract(SQLAlchemyObjectType):
    class Meta:
        model = ContractModel
        interfaces = (relay.Node,)


class Query(graphene.ObjectType):
    node = relay.Node.Field()

    # Get user
    getUser = graphene.List(lambda: User, id=graphene.ID(required=True))

    def resolve_getUser(self, info, id=None):
        query = User.get_query(info)
        if id:
            query = query.filter(UserModel.id == id)
        return query.all()


    # Get contract
    getContract = graphene.List(lambda: Contract, id=graphene.ID(required=True))

    def resolve_getContract(self, info, id=None):
        query = Contract.get_query(info)
        if id:
            query = query.filter(ContractModel.id == id)
        return query.all()



schema = graphene.Schema(query=Query)

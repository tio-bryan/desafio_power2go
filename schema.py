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
    user_id = graphene.Int(name='user_id')
    created_at = graphene.DateTime(name='created_at')

    class Meta:
        model = ContractModel
        interfaces = (relay.Node,)
        exclude_fields = ('user_id', 'created_at') # To show in snake case


    def resolve_user_id(self, _info):
        return self.user_id

    def resolve_created_at(self, _info):
        return self.created_at


class Query(graphene.ObjectType):
    node = relay.Node.Field()

    # Get user
    get_user = graphene.List(lambda: User, id=graphene.ID(required=True))

    def resolve_get_user(self, info, id=None):
        query = User.get_query(info)
        if id:
            query = query.filter(UserModel.id == id)
        return query.all()


    # Get contract
    get_contract = graphene.List(lambda: Contract, id=graphene.ID(required=True))

    def resolve_get_contract(self, info, id=None):
        query = Contract.get_query(info)
        if id:
            query = query.filter(ContractModel.id == id)
        return query.all()



schema = graphene.Schema(query=Query,)

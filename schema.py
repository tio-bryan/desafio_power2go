import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType
# from graphql import GraphQLError

from models import User as UserModel
from models import Contract as ContractModel
import api_utils


# Utils

# Get object variables
def get_obj_vars(class_name, obj):
    obj_vars = {}

    for k in vars(class_name).keys():
        if k[0] != '_':
            obj_vars[k] = getattr(obj, k)

    return obj_vars


# Objects
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
        exclude_fields = ('user_id', 'created_at') # Recreate fields to show in snake case

    def resolve_user_id(self, _info):
        return self.user_id

    def resolve_created_at(self, _info):
        return self.created_at


# Mutations

# Create user
class CreateUserInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    email = graphene.String()


class CreateUser(graphene.Mutation):
    class Arguments:
        input = CreateUserInput(required=True)

    for k, v in vars(CreateUserInput).items(): # Get CreateUserInput variables
        if k[0] != '_': # Remove private variables
            locals()[k] = v

    def mutate(self, _info, input):
        created_obj = api_utils.create(UserModel(**input))

        return CreateUser(**get_obj_vars(CreateUserInput, created_obj))


# Update user
class UpdateUserInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    email = graphene.String()


class UpdateUser(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        input = UpdateUserInput(required=True)

    for k, v in vars(UpdateUserInput).items(): # Get UpdateUserInput variables
        if k[0] != '_': # Remove private variables
            locals()[k] = v

    def mutate(self, _info, id, input):
        updated_obj = api_utils.update(UserModel, id, input)

        return UpdateUser(**get_obj_vars(UpdateUserInput, updated_obj))


# Delete user
class DeleteUser(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, _info, id):
        deleted_obj = api_utils.delete(UserModel, id)

        return DeleteUser(**deleted_obj)


# Create contract
class CreateContractInput(graphene.InputObjectType):
    id = graphene.ID()
    description = graphene.String()
    user_id = graphene.ID(name='user_id')
    created_at = graphene.DateTime(name='created_at')
    fidelity = graphene.Int()
    amount = graphene.Float()


class CreateContract(graphene.Mutation):
    class Arguments:
        input = CreateContractInput(required=True)

    for k, v in vars(CreateContractInput).items():
        if k[0] != '_':
            locals()[k] = v

    def mutate(self, _info, input=None):
        created_obj = api_utils.create(ContractModel(**input))

        return CreateContract(**get_obj_vars(CreateContractInput, created_obj))


# Update contract
class UpdateContractInput(graphene.InputObjectType):
    id = graphene.ID()
    description = graphene.String()
    user_id = graphene.ID(name='user_id')
    created_at = graphene.DateTime(name='created_at')
    fidelity = graphene.Int()
    amount = graphene.Float()

class UpdateContract(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        input = UpdateContractInput(required=True)

    for k, v in vars(UpdateContractInput).items(): # Get UpdateContractInput variables
        if k[0] != '_': # Remove private variables
            locals()[k] = v

    def mutate(self, _info, id, input):
        updated_obj = api_utils.update(ContractModel, id, input)

        return UpdateContract(**get_obj_vars(UpdateContractInput, updated_obj))


# Delete user
class DeleteContract(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, _info, id):
        deleted_obj = api_utils.delete(ContractModel, id)

        return DeleteContract(**deleted_obj)


class Mutations(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
    create_contract = CreateContract.Field()
    update_contract = UpdateContract.Field()
    delete_contract = DeleteContract.Field()


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


    # Get contract by user
    get_contracts_by_user = graphene.List(
        lambda: Contract,
        user_id=graphene.ID(name='user_id', required=True)
    )

    def resolve_get_contracts_by_user(self, info, user_id=None):
        query = Contract.get_query(info)
        if user_id:
            query = query.filter(ContractModel.user_id == user_id)
        return query.all()



schema = graphene.Schema(query=Query, mutation=Mutations)

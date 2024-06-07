import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType

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


class Contract(SQLAlchemyObjectType):
    user_id = graphene.Int(name='user_id')
    created_at = graphene.DateTime(name='created_at')
    modified_at = graphene.DateTime(name='modified_at')

    class Meta:
        model = ContractModel
        # Used relay to use pagination functions
        interfaces = (relay.Node,)
        # Recreate fields to show in snake case
        exclude_fields = ('user_id', 'created_at', 'modified_at')

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
    created_at = graphene.DateTime(name='created_at')
    modified_at = graphene.DateTime(name='modified_at')

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
    created_at = graphene.DateTime(name='created_at')
    modified_at = graphene.DateTime(name='modified_at')


class UpdateUser(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        input = UpdateUserInput(required=True)

    for k, v in vars(UpdateUserInput).items():
        if k[0] != '_':
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
        # Check if has linked contracts.
        # Maybe is there a more elegant way to implement this on DB side.
        api_utils.get_contracts_by_user_id(ContractModel, id)
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
        # Check if user exists before creating contract.
        # I tried to do this from DB side, but I couldn't.
        api_utils.get_by_id(UserModel, input.user_id)
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
        # Check if user exists before updating contract.
        api_utils.get_by_id(UserModel, input.user_id)
        updated_obj = api_utils.update(ContractModel, id, input)

        return UpdateContract(**get_obj_vars(UpdateContractInput, updated_obj))


# Delete contract
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
    get_user = graphene.Field(User, id=graphene.ID(required=True))

    def resolve_get_user(self, _info, id=None):
        return api_utils.get_by_id(UserModel, id)


    # Get contract
    get_contract = graphene.Field(Contract, id=graphene.ID(required=True))

    def resolve_get_contract(self, _info, id=None):
        return api_utils.get_by_id(ContractModel, id)


    # Get contract by user. Wrong implementation because it's the same of getUser but work with
    # default graphQL pagination on Contracts object: https://graphql.org/learn/pagination/

    # Works with following query format:
    query = """
    query getContractsByUser($user_id: ID!) {
        getContractsByUser(user_id: $user_id) {
            Contracts {
                edges {
                    node {
                        id
                    }
                }
            } 
        }
    }
    """
    get_contracts_by_user = graphene.Field(
        User,
        user_id=graphene.ID(name='user_id', required=True)
    )

    def resolve_get_contracts_by_user(self, _info, user_id=None):
        return api_utils.get_by_id(UserModel, user_id)


schema = graphene.Schema(query=Query, mutation=Mutations)

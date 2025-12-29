import graphene
from graphene_django import DjangoObjectType
from crm.models import Customer

# GraphQL type for Customer model
class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer

# Input type for creating customer
class CustomerInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String()

# Mutation
class CreateCustomer(graphene.Mutation):
    class Arguments:
        input = CustomerInput(required=True)

    customer = graphene.Field(CustomerType)
    message = graphene.String()

    def mutate(root, info, input):
        # Basic email uniqueness check
        if Customer.objects.filter(email=input.email).exists():
            return CreateCustomer(customer=None, message="Email already exists")
        
        customer = Customer(
            name=input.name,
            email=input.email,
            phone=input.phone
        )
        customer.save()
        return CreateCustomer(customer=customer, message="Customer created successfully")

# Query class
class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hello, GraphQL!")

# Add to Mutation class
class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()

# Schema
schema = graphene.Schema(query=Query, mutation=Mutation)

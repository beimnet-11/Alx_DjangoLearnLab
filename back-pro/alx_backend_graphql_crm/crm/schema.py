import graphene
from graphene_django import DjangoObjectType
from .models import Customer

# GraphQL type for Customer
class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = ("id", "name", "email", "phone")

# Input type for creating customer
class CreateCustomerInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String()

# Mutation
class CreateCustomer(graphene.Mutation):
    class Arguments:
        input = CreateCustomerInput(required=True)

    customer = graphene.Field(CustomerType)
    message = graphene.String()

    def mutate(self, info, input):
        customer = Customer.objects.create(
            name=input.name,
            email=input.email,
            phone=input.phone
        )
        return CreateCustomer(customer=customer, message="Customer created successfully!")

# Query
class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hello, GraphQL!")

# Mutation class
class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()

# Schema
schema = graphene.Schema(query=Query, mutation=Mutation)

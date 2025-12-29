import graphene
from crm.schema import Query as CRMQuery

# You can combine multiple query classes if needed
class Query(CRMQuery, graphene.ObjectType):
    pass

# Define the schema
schema = graphene.Schema(query=Query)

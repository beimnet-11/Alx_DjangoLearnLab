import graphene
from graphene_django import DjangoObjectType
from django.db import transaction
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re
from decimal import Decimal
from .models import Customer, Product, Order

# GraphQL Types
class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = ("id", "name", "email", "phone")

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("id", "name", "price", "stock")

class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = ("id", "customer", "products", "order_date", "total_amount")

# Input Types
class CustomerInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String()

class ProductInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    price = graphene.Decimal(required=True)
    stock = graphene.Int()

class BulkCustomerInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String()

class OrderInput(graphene.InputObjectType):
    customer_id = graphene.ID(required=True)
    product_ids = graphene.List(graphene.ID, required=True)
    order_date = graphene.DateTime()

# Helper function for phone validation
def validate_phone(phone):
    if phone:
        # Accept formats: +1234567890 or 123-456-7890
        pattern = r'^(\+\d{10,15}|\d{3}-\d{3}-\d{4})$'
        if not re.match(pattern, phone):
            raise ValidationError("Phone must be in format +1234567890 or 123-456-7890")
    return phone

# Mutations
class CreateCustomer(graphene.Mutation):
    class Arguments:
        input = CustomerInput(required=True)

    customer = graphene.Field(CustomerType)
    message = graphene.String()

    def mutate(root, info, input):
        # Validate email uniqueness
        if Customer.objects.filter(email=input.email).exists():
            return CreateCustomer(customer=None, message="Email already exists")
        
        # Validate phone format
        try:
            validated_phone = validate_phone(input.phone) if input.phone else None
        except ValidationError as e:
            return CreateCustomer(customer=None, message=str(e))
        
        # Validate email format
        try:
            validate_email(input.email)
        except ValidationError:
            return CreateCustomer(customer=None, message="Invalid email format")
        
        customer = Customer(
            name=input.name,
            email=input.email,
            phone=validated_phone
        )
        customer.save()
        return CreateCustomer(customer=customer, message="Customer created successfully")

class BulkCreateCustomers(graphene.Mutation):
    class Arguments:
        input = graphene.List(BulkCustomerInput, required=True)

    customers = graphene.List(CustomerType)
    errors = graphene.List(graphene.String)

    @transaction.atomic
    def mutate(root, info, input):
        customers = []
        errors = []
        
        for idx, customer_data in enumerate(input):
            try:
                # Validate email uniqueness
                if Customer.objects.filter(email=customer_data.email).exists():
                    errors.append(f"Row {idx + 1}: Email '{customer_data.email}' already exists")
                    continue
                
                # Validate phone format
                validated_phone = None
                if customer_data.phone:
                    try:
                        validated_phone = validate_phone(customer_data.phone)
                    except ValidationError as e:
                        errors.append(f"Row {idx + 1}: {str(e)}")
                        continue
                
                # Validate email format
                try:
                    validate_email(customer_data.email)
                except ValidationError:
                    errors.append(f"Row {idx + 1}: Invalid email format")
                    continue
                
                customer = Customer(
                    name=customer_data.name,
                    email=customer_data.email,
                    phone=validated_phone
                )
                customer.save()
                customers.append(customer)
            except Exception as e:
                errors.append(f"Row {idx + 1}: {str(e)}")
        
        return BulkCreateCustomers(customers=customers, errors=errors)

class CreateProduct(graphene.Mutation):
    class Arguments:
        input = ProductInput(required=True)

    product = graphene.Field(ProductType)
    message = graphene.String()

    def mutate(root, info, input):
        # Validate price is positive
        if input.price <= 0:
            return CreateProduct(product=None, message="Price must be positive")
        
        # Validate stock is non-negative
        stock = input.stock if input.stock is not None else 0
        if stock < 0:
            return CreateProduct(product=None, message="Stock cannot be negative")
        
        product = Product(
            name=input.name,
            price=input.price,
            stock=stock
        )
        product.save()
        return CreateProduct(product=product, message="Product created successfully")

class CreateOrder(graphene.Mutation):
    class Arguments:
        input = OrderInput(required=True)

    order = graphene.Field(OrderType)
    message = graphene.String()

    def mutate(root, info, input):
        # Validate customer exists
        try:
            customer = Customer.objects.get(pk=input.customer_id)
        except Customer.DoesNotExist:
            return CreateOrder(order=None, message=f"Customer with ID {input.customer_id} does not exist")
        
        # Validate at least one product
        if not input.product_ids or len(input.product_ids) == 0:
            return CreateOrder(order=None, message="At least one product must be selected")
        
        # Validate all products exist
        try:
            products = Product.objects.filter(pk__in=input.product_ids)
            if products.count() != len(input.product_ids):
                missing_ids = set(input.product_ids) - set(str(p.id) for p in products)
                return CreateOrder(order=None, message=f"Invalid product IDs: {', '.join(missing_ids)}")
        except Exception as e:
            return CreateOrder(order=None, message=f"Error validating products: {str(e)}")
        
        # Calculate total amount
        total_amount = sum(product.price for product in products)
        
        # Create order
        order = Order(
            customer=customer,
            total_amount=total_amount
        )
        if input.order_date:
            order.order_date = input.order_date
        order.save()
        
        # Associate products
        order.products.set(products)
        
        return CreateOrder(order=order, message="Order created successfully")

# Query class
class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hello, GraphQL!")

# Mutation class
class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()

# Schema
schema = graphene.Schema(query=Query, mutation=Mutation)

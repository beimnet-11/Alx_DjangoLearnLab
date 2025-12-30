#!/usr/bin/env python
"""
Seed script for populating the CRM database with sample data.
Run with: python manage.py shell < seed_db.py
Or: python seed_db.py (if Django is configured)
"""
import os
import django
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_graphql_crm.settings')
django.setup()

from crm.models import Customer, Product, Order

def seed_database():
    """Seed the database with sample data"""
    
    # Clear existing data (optional - comment out if you want to keep existing data)
    print("Clearing existing data...")
    Order.objects.all().delete()
    Product.objects.all().delete()
    Customer.objects.all().delete()
    
    # Create Customers
    print("Creating customers...")
    customers_data = [
        {"name": "Alice Johnson", "email": "alice@example.com", "phone": "+1234567890"},
        {"name": "Bob Smith", "email": "bob@example.com", "phone": "123-456-7890"},
        {"name": "Carol Williams", "email": "carol@example.com", "phone": "+1987654321"},
        {"name": "David Brown", "email": "david@example.com", "phone": "555-123-4567"},
        {"name": "Eva Davis", "email": "eva@example.com", "phone": "+1555123456"},
    ]
    
    customers = []
    for data in customers_data:
        customer, created = Customer.objects.get_or_create(
            email=data["email"],
            defaults={"name": data["name"], "phone": data["phone"]}
        )
        customers.append(customer)
        if created:
            print(f"  Created customer: {customer.name}")
        else:
            print(f"  Customer already exists: {customer.name}")
    
    # Create Products
    print("\nCreating products...")
    products_data = [
        {"name": "Laptop", "price": Decimal("999.99"), "stock": 10},
        {"name": "Mouse", "price": Decimal("29.99"), "stock": 50},
        {"name": "Keyboard", "price": Decimal("79.99"), "stock": 30},
        {"name": "Monitor", "price": Decimal("299.99"), "stock": 15},
        {"name": "Webcam", "price": Decimal("49.99"), "stock": 25},
        {"name": "Headphones", "price": Decimal("129.99"), "stock": 20},
    ]
    
    products = []
    for data in products_data:
        product, created = Product.objects.get_or_create(
            name=data["name"],
            defaults={"price": data["price"], "stock": data["stock"]}
        )
        products.append(product)
        if created:
            print(f"  Created product: {product.name} - ${product.price}")
        else:
            print(f"  Product already exists: {product.name}")
    
    # Create Orders
    print("\nCreating orders...")
    orders_data = [
        {
            "customer": customers[0],  # Alice
            "products": [products[0], products[1], products[2]],  # Laptop, Mouse, Keyboard
        },
        {
            "customer": customers[1],  # Bob
            "products": [products[3], products[4]],  # Monitor, Webcam
        },
        {
            "customer": customers[2],  # Carol
            "products": [products[5]],  # Headphones
        },
        {
            "customer": customers[0],  # Alice (second order)
            "products": [products[4], products[5]],  # Webcam, Headphones
        },
    ]
    
    for order_data in orders_data:
        order = Order.objects.create(customer=order_data["customer"])
        order.products.set(order_data["products"])
        
        # Calculate and set total amount
        total = sum(product.price for product in order_data["products"])
        order.total_amount = total
        order.save()
        
        product_names = ", ".join([p.name for p in order_data["products"]])
        print(f"  Created order #{order.id} for {order.customer.name}: {product_names} - Total: ${order.total_amount}")
    
    print("\n" + "="*50)
    print("Database seeding completed!")
    print("="*50)
    print(f"Customers: {Customer.objects.count()}")
    print(f"Products: {Product.objects.count()}")
    print(f"Orders: {Order.objects.count()}")

if __name__ == "__main__":
    seed_database()


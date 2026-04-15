"""Database models for E-Battisseurs"""
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Supplier(Base):
    __tablename__ = "suppliers"
    
    id = Column(String(50), primary_key=True)
    name = Column(String(200))
    products_count = Column(Integer, default=0)
    rating = Column(Float, default=4.5)
    status = Column(String(20), default="active")
    created_at = Column(DateTime, default=datetime.utcnow)

class Product(Base):
    __tablename__ = "products"
    
    id = Column(String(50), primary_key=True)
    supplier_id = Column(String(50), ForeignKey("suppliers.id"))
    supplier_product_id = Column(String(100))
    title = Column(String(500))
    description = Column(Text)
    price = Column(Float)
    compare_at_price = Column(Float)
    currency = Column(String(10), default="USD")
    category = Column(String(100))
    subcategory = Column(String(100))
    images = Column(JSON)
    options = Column(JSON)
    variants = Column(JSON)
    inventory = Column(Integer, default=0)
    weight = Column(Float)
    dimensions = Column(JSON)
    tags = Column(JSON)
    status = Column(String(20), default="active")
    created_at = Column(DateTime, default=datetime.utcnow)

class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(String(50), primary_key=True)
    email = Column(String(200), unique=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    phone = Column(String(50))
    country = Column(String(10))
    total_orders = Column(Integer, default=0)
    total_spent = Column(Float, default=0.0)
    status = Column(String(20), default="active")
    tags = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(String(50), primary_key=True)
    order_number = Column(String(50), unique=True)
    customer_id = Column(String(50), ForeignKey("customers.id"))
    items = Column(JSON)
    subtotal = Column(Float)
    shipping_cost = Column(Float)
    tax_amount = Column(Float)
    discount_amount = Column(Float)
    total = Column(Float)
    currency = Column(String(10), default="USD")
    status = Column(String(20), default="pending")
    shipping_address = Column(JSON)
    supplier_id = Column(String(50))
    tracking_number = Column(String(100))
    carrier = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(String(50), primary_key=True)
    order_id = Column(String(50), ForeignKey("orders.id"))
    customer_id = Column(String(50))
    amount = Column(Float)
    currency = Column(String(10))
    status = Column(String(20))
    method = Column(JSON)
    transaction_id = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)

class Ticket(Base):
    __tablename__ = "tickets"
    
    id = Column(String(50), primary_key=True)
    customer_id = Column(String(50))
    subject = Column(String(500))
    description = Column(Text)
    status = Column(String(20), default="open")
    priority = Column(String(20), default="medium")
    assigned_to = Column(String(100))
    messages = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

class Campaign(Base):
    __tablename__ = "campaigns"
    
    id = Column(String(50), primary_key=True)
    name = Column(String(200))
    type = Column(String(20))
    status = Column(String(20), default="draft")
    audience_size = Column(Integer, default=0)
    budget = Column(Float)
    sent = Column(Integer, default=0)
    opened = Column(Integer, default=0)
    clicked = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

class Affiliate(Base):
    __tablename__ = "affiliates"
    
    id = Column(String(50), primary_key=True)
    name = Column(String(200))
    email = Column(String(200), unique=True)
    level = Column(Integer, default=1)
    parent_id = Column(String(50))
    commission_rate = Column(Float, default=10.0)
    total_sales = Column(Float, default=0.0)
    total_commission = Column(Float, default=0.0)
    status = Column(String(20), default="active")
    joined_at = Column(DateTime, default=datetime.utcnow)

class Agent(Base):
    __tablename__ = "agents"
    
    id = Column(String(50), primary_key=True)
    name = Column(String(200))
    description = Column(Text)
    status = Column(String(20), default="idle")
    webhook_url = Column(String(500))
    last_run = Column(DateTime)


# Database setup
def init_db(database_url: str):
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    return engine

def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from contextlib import contextmanager
from models import Category, Supplier, Product

# Define the database connection string based on your setup
DATABASE_URL = "sqlite:///../Alvike.db"

# Create a SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a SessionLocal class for interacting with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rest of your functions
def get_categories(db):
    return db.query(Category).all()

def get_suppliers(db):
    return db.query(Supplier).all()

def get_products(db):
    return db.query(Product).all()

def add_product(db, name, color, size, quantity_in_stock, unit_price, category_id, supplier_id):
    new_product = Product(
        name=name,
        color=color,
        size=size,
        quantity_in_stock=quantity_in_stock,
        unit_price=unit_price,
        category_id=category_id,
        supplier_id=supplier_id
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

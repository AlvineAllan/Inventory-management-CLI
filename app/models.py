
from sqlalchemy import Column, Integer, String,Boolean, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    is_active = Column(Boolean)
    
    # relationship definition
    products = relationship("Product", back_populates="category")

class Supplier(Base):
    __tablename__ = 'suppliers'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    contact_person = Column(String)
    contact_email = Column(String)
    contact_phone = Column(String)
    
    # relationship definition
    products = relationship("Product", back_populates="supplier")

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    color = Column(String)
    size = Column(String)
    quantity_in_stock = Column(Integer)
    unit_price = Column(Integer)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship("Category", back_populates="products")
    supplier_id = Column(Integer, ForeignKey('suppliers.id'))
    supplier = relationship("Supplier", back_populates="products")

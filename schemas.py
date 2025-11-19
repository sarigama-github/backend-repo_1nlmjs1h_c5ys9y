"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# North Indian Restaurant Schemas

class Dish(BaseModel):
    """
    Menu dishes collection
    Collection name: "dish"
    """
    name: str = Field(..., description="Dish name")
    description: Optional[str] = Field(None, description="Short description of the dish")
    price: float = Field(..., ge=0, description="Price in local currency")
    category: str = Field(..., description="Category like Curry, Tandoor, Breads, Sweets, Beverages")
    spicy_level: Optional[int] = Field(None, ge=0, le=5, description="Spice level from 0-5")
    vegetarian: bool = Field(False, description="Is this dish vegetarian")
    image: Optional[str] = Field(None, description="Public image URL")

class Reservation(BaseModel):
    """
    Reservations collection
    Collection name: "reservation"
    """
    name: str = Field(..., description="Guest name")
    phone: str = Field(..., description="Contact phone number")
    party_size: int = Field(..., ge=1, le=20, description="Number of guests")
    date: date = Field(..., description="Reservation date")
    time: str = Field(..., description="Reservation time, e.g., 19:30")
    special_requests: Optional[str] = Field(None, description="Any special notes")

# Add your own schemas here:
# --------------------------------------------------

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!

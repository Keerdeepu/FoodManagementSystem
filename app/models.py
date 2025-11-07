# app/models.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DECIMAL, TIMESTAMP
from sqlalchemy.orm import relationship
from .db import Base
from sqlalchemy.sql import func

class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    servings = Column(Integer, default=1)
    prep_time_minutes = Column(Integer, default=0)
    cook_time_minutes = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    steps = relationship("Step", cascade="all, delete-orphan", back_populates="recipe")
    recipe_ingredients = relationship("RecipeIngredient", cascade="all, delete-orphan", back_populates="recipe")

class Ingredient(Base):
    __tablename__ = "ingredients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    unit = Column(String(50), default='unit')
    created_at = Column(TIMESTAMP, server_default=func.now())

    recipe_ingredients = relationship("RecipeIngredient", back_populates="ingredient")

class Step(Base):
    __tablename__ = "steps"
    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id", ondelete="CASCADE"), nullable=False)
    step_number = Column(Integer, nullable=False)
    instruction = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    recipe = relationship("Recipe", back_populates="steps")

class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"
    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id", ondelete="CASCADE"), nullable=False)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(DECIMAL(10,2), default=0)
    note = Column(String(255))
    created_at = Column(TIMESTAMP, server_default=func.now())

    recipe = relationship("Recipe", back_populates="recipe_ingredients")
    ingredient = relationship("Ingredient", back_populates="recipe_ingredients")

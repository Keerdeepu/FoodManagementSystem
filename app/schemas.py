# app/schemas.py
from typing import List, Optional
from pydantic import BaseModel

class StepBase(BaseModel):
    step_number: int
    instruction: str

class StepCreate(StepBase):
    pass

class Step(StepBase):
    id: int
    recipe_id: int

    class Config:
        orm_mode = True

class IngredientBase(BaseModel):
    name: str
    unit: Optional[str] = 'unit'

class IngredientCreate(IngredientBase):
    pass

class Ingredient(IngredientBase):
    id: int

    class Config:
        orm_mode = True

class RecipeIngredientBase(BaseModel):
    ingredient_id: int
    quantity: float
    note: Optional[str] = None

class RecipeIngredientCreate(RecipeIngredientBase):
    pass

class RecipeIngredient(RecipeIngredientBase):
    id: int
    recipe_id: int
    ingredient: Ingredient

    class Config:
        orm_mode = True

class RecipeBase(BaseModel):
    title: str
    description: Optional[str] = None
    servings: Optional[int] = 1
    prep_time_minutes: Optional[int] = 0
    cook_time_minutes: Optional[int] = 0

class RecipeCreate(RecipeBase):
    steps: Optional[List[StepCreate]] = []
    ingredients: Optional[List[RecipeIngredientCreate]] = []

class Recipe(RecipeBase):
    id: int
    steps: List[Step] = []
    recipe_ingredients: List[RecipeIngredient] = []

    class Config:
        orm_mode = True

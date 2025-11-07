# app/main.py
from fastapi import FastAPI, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .db import engine, Base, get_db

# Create tables (if you prefer SQL files, you can skip this)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Food Recipe Management System")

@app.post("/ingredients/", response_model=schemas.Ingredient)
def create_ingredient(ingredient: schemas.IngredientCreate, db: Session = Depends(get_db)):
    return crud.create_ingredient(db, ingredient)

@app.get("/ingredients/", response_model=List[schemas.Ingredient])
def list_ingredients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_ingredients(db, skip=skip, limit=limit)

@app.post("/recipes/", response_model=schemas.Recipe)
def create_recipe(recipe: schemas.RecipeCreate, db: Session = Depends(get_db)):
    return crud.create_recipe(db, recipe)

@app.get("/recipes/", response_model=List[schemas.Recipe])
def list_recipes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_recipes(db, skip=skip, limit=limit)

@app.get("/recipes/{recipe_id}", response_model=schemas.Recipe)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = crud.get_recipe(db, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

@app.put("/recipes/{recipe_id}", response_model=schemas.Recipe)
def put_recipe(recipe_id: int, recipe: schemas.RecipeCreate, db: Session = Depends(get_db)):
    updated = crud.update_recipe(db, recipe_id, recipe)
    if not updated:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return updated

@app.delete("/recipes/{recipe_id}")
def remove_recipe(recipe_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_recipe(db, recipe_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return {"message": "deleted"}

# Simple health check
@app.get("/")
def root():
    return {"message": "Food Recipe Management API is running"}

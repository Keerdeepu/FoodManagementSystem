# app/crud.py
from sqlalchemy.orm import Session
from . import models, schemas
from sqlalchemy.exc import IntegrityError

# --- Ingredient CRUD ---
def get_ingredient_by_name(db: Session, name: str):
    return db.query(models.Ingredient).filter(models.Ingredient.name == name).first()

def create_ingredient(db: Session, ingredient: schemas.IngredientCreate):
    db_obj = models.Ingredient(name=ingredient.name.strip(), unit=ingredient.unit)
    db.add(db_obj)
    try:
        db.commit()
        db.refresh(db_obj)
        return db_obj
    except IntegrityError:
        db.rollback()
        return get_ingredient_by_name(db, ingredient.name.strip())

def get_ingredients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Ingredient).offset(skip).limit(limit).all()

# --- Recipe CRUD ---
def create_recipe(db: Session, recipe: schemas.RecipeCreate):
    db_recipe = models.Recipe(
        title=recipe.title.strip(),
        description=recipe.description,
        servings=recipe.servings,
        prep_time_minutes=recipe.prep_time_minutes,
        cook_time_minutes=recipe.cook_time_minutes
    )
    db.add(db_recipe)
    db.flush()  # get id for relationships

    # Steps
    for s in recipe.steps or []:
        db_step = models.Step(recipe_id=db_recipe.id, step_number=s.step_number, instruction=s.instruction)
        db.add(db_step)

    # Ingredients: ensure ingredient exists, then link
    for ing in recipe.ingredients or []:
        existing = db.query(models.Ingredient).filter(models.Ingredient.id == ing.ingredient_id).first()
        if not existing:
            # If ingredient with id not found, skip or raise
            continue
        ri = models.RecipeIngredient(recipe_id=db_recipe.id, ingredient_id=ing.ingredient_id, quantity=ing.quantity, note=ing.note)
        db.add(ri)

    db.commit()
    db.refresh(db_recipe)
    return db_recipe

def get_recipe(db: Session, recipe_id: int):
    return db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()

def get_recipes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Recipe).offset(skip).limit(limit).all()

def update_recipe(db: Session, recipe_id: int, recipe: schemas.RecipeCreate):
    db_recipe = get_recipe(db, recipe_id)
    if not db_recipe:
        return None
    db_recipe.title = recipe.title or db_recipe.title
    db_recipe.description = recipe.description or db_recipe.description
    db_recipe.servings = recipe.servings or db_recipe.servings
    db_recipe.prep_time_minutes = recipe.prep_time_minutes or db_recipe.prep_time_minutes
    db_recipe.cook_time_minutes = recipe.cook_time_minutes or db_recipe.cook_time_minutes

    # Replace steps and ingredients (simple approach)
    db.query(models.Step).filter(models.Step.recipe_id == db_recipe.id).delete()
    db.query(models.RecipeIngredient).filter(models.RecipeIngredient.recipe_id == db_recipe.id).delete()

    for s in recipe.steps or []:
        db_step = models.Step(recipe_id=db_recipe.id, step_number=s.step_number, instruction=s.instruction)
        db.add(db_step)
    for ing in recipe.ingredients or []:
        ri = models.RecipeIngredient(recipe_id=db_recipe.id, ingredient_id=ing.ingredient_id, quantity=ing.quantity, note=ing.note)
        db.add(ri)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

def delete_recipe(db: Session, recipe_id: int):
    db_recipe = get_recipe(db, recipe_id)
    if not db_recipe:
        return False
    db.delete(db_recipe)
    db.commit()
    return True

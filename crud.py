from sqlalchemy.orm import Session
import models, schemas

# Supporting functions

# Ingredient table CRUD
def get_ingredient(db: Session, ingredient_name: str):
    return db.query(models.Ingredient).filter(
        models.Ingredient.name == ingredient_name).first()
    
def get_ingredients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Ingredient).offset(skip).limit(limit).all()

def create_ingredient(db: Session, ingredient: schemas.IngredientCreate):
    db_ingredient = models.Ingredient(
        name=ingredient.name,
        ingredient_type_id=ingredient.ingredient_type_id, 
        **ingredient.nutritional_values.dict())
    db.add(db_ingredient)
    db.commit()
    db.refresh(db_ingredient)
    return db_ingredient

# Ingredient Type table CRUD
def get_ingredient_type(db: Session, type_name: str):
    return db.query(models.IngredientType).filter(
        models.IngredientType.name == type_name).first()

def get_ingredient_type_by_id(db: Session, type_id: int):
    return db.query(models.IngredientType).filter(
        models.IngredientType.id == type_id).first()

def get_ingredient_types(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.IngredientType).offset(skip).limit(limit).all()

def create_ingredient_type(db: Session, ingredient_type: schemas.IngredientTypeCreate):
    db_type = models.IngredientType(name=ingredient_type.name)
    db.add(db_type)
    db.commit()
    db.refresh(db_type)
    return db_type



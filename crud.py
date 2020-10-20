from sqlalchemy.orm import Session
import models, schemas

# Supporting functions

# Cooking Unit table CRUD
def get_unit(db: Session, unit_name: str):
    return db.query(models.CookingUnit).filter(
        models.CookingUnit.name == unit_name).first()

def get_units(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.CookingUnit).offset(skip).limit(limit).all()

def create_unit(db: Session, unit: schemas.CookingUnitCreate):
    db_unit = models.CookingUnit(**unit.dict())
    db.add(db_unit)
    db.commit()
    db.refresh(db_unit)
    return db_unit

# Ingredient table CRUD
def get_ingredient(db: Session, ingredient_name: str):
    return db.query(models.Ingredient).filter(
        models.Ingredient.name == ingredient_name).first()
    
def get_ingredients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Ingredient).offset(skip).limit(limit).all()

def create_ingredient(db: Session, ingredient: schemas.IngredientCreate):
    if ingredient.category:
        db_type = db.query(models.IngredientType).filter(
            models.IngredientType.name == ingredient.category).first()
    db_ingredient = models.Ingredient(
        name=ingredient.name,
        ingredient_type_id=[db_type.id if ingredient.category else None][0], 
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

def update_ingredient_type(db: Session, type_name: str, new_name: schemas.IngredientTypeUpdate):
    db_type = db.query(models.IngredientType).filter(
        models.IngredientType.name == type_name).first()
    db_type.name = new_name.name
    db.commit()
    return db_type

def delete_ingredient_type(db: Session, type_name: str):
    db_type = db.query(models.IngredientType).filter(
        models.IngredientType.name == type_name).first()
    db.delete(db_type)
    db.commit()

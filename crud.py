from sqlalchemy.orm import Session
import models, schemas

# Supporting functions
def custom_ingredient_response(db_query):
    return {
        "id": db_query.id,
        "name": db_query.name,
        "ingredient_type_id": db_query.ingredient_type_id,
        "nutritional_values": {
            "calories": db_query.calories,
            "saturated_fat": db_query.saturated_fat,
            "trans_fat": db_query.trans_fat,
            "cholesterol": db_query.cholesterol,
            "sodium": db_query.sodium,
            "carbohydrate": db_query.carbohydrate,
            "sugar": db_query.sugar,
            "protein": db_query.protein
        }
    }

# Ingredient table CRUD
def get_ingredient(db: Session, ingredient_name: str):
    query_result = db.query(models.Ingredient).filter(
        models.Ingredient.name == ingredient_name).first()
    if query_result is not None:
        return custom_ingredient_response(query_result)
    return query_result

def get_ingredients(db: Session, skip: int = 0, limit: int = 100):
    query_result = db.query(models.Ingredient).offset(skip).limit(limit).all()
    if query_result is not None:
        response_object = []
        for entry in query_result:
            response_object.append(custom_ingredient_response(entry))
        return response_object
    return query_result

def create_ingredient(db: Session, ingredient: schemas.IngredientCreate):
    db_ingredient = models.Ingredient(
        name=ingredient.name,
        ingredient_type_id=ingredient.ingredient_type_id, 
        **ingredient.nutritional_values.dict())
    db.add(db_ingredient)
    db.commit()
    db.refresh(db_ingredient)
    return custom_ingredient_response(db_ingredient)

# Ingredient Type table CRUD
def get_ingredient_type(db: Session, type_name: str):
    return db.query(models.IngredientType).filter(
        models.IngredientType.name == type_name).first()

def get_ingredient_types(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.IngredientType).offset(skip).limit(limit).all()

def create_ingredient_type(db: Session, ingredient_type: schemas.IngredientTypeCreate):
    db_type = models.IngredientType(name=ingredient_type.name)
    db.add(db_type)
    db.commit()
    db.refresh(db_type)
    return db_type



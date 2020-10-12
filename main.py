from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Cooking Unit Path Operations
@app.get("/unit/", response_model=List[schemas.CookingUnit])
def read_units(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    units = crud.get_units(db=db, skip=skip, limit=limit)
    return units

@app.get("/unit/{unit_name}", response_model=schemas.CookingUnit)
def read_unit(unit_name: str, db: Session = Depends(get_db)):
    db_unit = crud.get_unit(db=db, unit_name=unit_name)
    if db_unit is None:
        raise HTTPException(status_code=404, detail="Unit not found")
    return db_unit

@app.post("/unit/", response_model=schemas.CookingUnit)
def create_unit(unit: schemas.CookingUnitCreate, db: Session = Depends(get_db)):
    db_unit = crud.get_unit(db=db, unit_name=unit.name)
    if db_unit:
        raise HTTPException(status_code=400, detail="Unit already exists")
    return crud.create_unit(db=db, unit=unit)

# Ingredient Type Path Operations
@app.get("/ingredienttype/", response_model=List[schemas.IngredientType])
def read_ingredient_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    types = crud.get_ingredient_types(db=db, skip=skip, limit=limit)
    return types

@app.get("/ingredienttype/{type_name}", response_model=schemas.IngredientType)
def read_ingredient_type(type_name: str, db: Session = Depends(get_db)):
    db_type = crud.get_ingredient_type(db=db, type_name=type_name)
    if db_type is None:
        raise HTTPException(status_code=404, detail="Ingredient type not found")
    return db_type

@app.post("/ingredienttype/", response_model=schemas.IngredientType)
def create_ingredient_type(ingredient_type: schemas.IngredientTypeCreate, db: Session = Depends(get_db)):
    db_type = crud.get_ingredient_type(db=db, type_name=ingredient_type.name)
    if db_type:
        raise HTTPException(status_code=400, detail="Ingredient type already exists")
    return crud.create_ingredient_type(db=db, ingredient_type=ingredient_type)

@app.put("/ingredienttype/{type_name}", response_model=schemas.IngredientType)
def update_ingredient_type(type_name: str, new_name: schemas.IngredientTypeUpdate, db: Session = Depends(get_db)):
    db_current_type = crud.get_ingredient_type(db=db, type_name=type_name)
    if db_current_type is None:
        raise HTTPException(status_code=404, detail="Ingredient type not found")
    return crud.update_ingredient_type(db=db, type_name=type_name, new_name=new_name)

@app.delete("/ingredienttype/{type_name}")
def delete_ingredient_type(type_name: str, db: Session = Depends(get_db)):
    db_current_type = crud.get_ingredient_type(db=db, type_name=type_name)
    if db_current_type is None:
        raise HTTPException(status_code=404, detail="Ingredient type not found")
    crud.delete_ingredient_type(db=db, type_name=type_name)
    return {"detail": f"Ingredient type: {type_name} -> deleted", "status_code": 204}

# Ingredient Path Operations
@app.get("/ingredient/", response_model=List[schemas.Ingredient])
def read_ingredients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    ingredients = crud.get_ingredients(db=db, skip=skip, limit=limit)
    return ingredients

@app.get("/ingredient/{ingredient_name}", response_model=schemas.Ingredient)
def read_ingredient(ingredient_name: str, db: Session = Depends(get_db)):
    db_ingredient = crud.get_ingredient(db=db, ingredient_name=ingredient_name)
    if db_ingredient is None:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return db_ingredient

@app.post("/ingredient/", response_model=schemas.Ingredient)
def create_ingredient(ingredient: schemas.IngredientCreate, db: Session = Depends(get_db)):
    # Make this take a string for ingredient type
    db_ingredient = crud.get_ingredient(db=db, ingredient_name=ingredient.name)
    db_type = crud.get_ingredient_type_by_id(db, type_id=ingredient.ingredient_type_id)
    #db_type = get_ingredient_type(db,)
    if db_ingredient:
        raise HTTPException(status_code=400, detail="Ingredient already exists")
    if not db_type:
        raise HTTPException(status_code=404, detail="Ingredient type not found")
    return crud.create_ingredient(db=db, ingredient=ingredient)
from pydantic import BaseModel, Schema
from typing import Optional, List, Dict
from humps import camel

def to_camel(string):
    return camel.case(string)

# General purpose Schemas
class CamelModel(BaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


# Ingredient Schemas
class NutritionalValues(CamelModel):
    # Find a way to get this working
    calories: int
    saturated_fat: int
    trans_fat: int
    cholesterol: int
    sodium: int
    carbohydrate: int
    sugar: int
    protein: int         

class IngredientBase(CamelModel):
    name: str
    ingredient_type_id: int
    nutritional_values: Optional[NutritionalValues] = None
    
    class Config:
        orm_mode = True

class IngredientCreate(IngredientBase):
    # Create Operation
    pass

class Ingredient(IngredientBase):
    # Read Operation
    id: int

class IngredientSubQuery(CamelModel):
    # Read Operation
    id: int
    name: str
    
    class Config:
        orm_mode = True


# Ingredient Type Schemas
class IngredientTypeBase(CamelModel):
    name: str

class IngredientTypeCreate(IngredientTypeBase):
    # Create Operation
    pass

class IngredientType(IngredientTypeBase):
    # Read Operation
    id: int
    ingredients: List[IngredientSubQuery] = []

    class Config:
        orm_mode = True
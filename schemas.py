from pydantic import BaseModel, Schema, root_validator, validator, PositiveInt
from pydantic.utils import GetterDict
from typing import Optional, List, Dict

def to_camel(string: str) -> str:
    first, *others = string.split('_')
    return ''.join([first.lower(), *map(str.title, others)])

# General purpose stuff
class CamelModel(BaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True

class MyGetterDict(GetterDict):  # create a custom GetterDict to be able to add new keys
    def __setitem__(self, key, value):
        return setattr(self._obj, key, value)

# Ingredient Schemas
class NutritionalValues(CamelModel):
    calories: PositiveInt
    saturated_fat: PositiveInt
    trans_fat: PositiveInt
    cholesterol: PositiveInt
    sodium: PositiveInt
    carbohydrate: PositiveInt
    sugar: PositiveInt
    protein: PositiveInt         

class IngredientBase(CamelModel):
    name: str
    ingredient_type_id: int
    nutritional_values: NutritionalValues
    
    class Config:
        orm_mode = True

class IngredientCreate(IngredientBase):
    # Create Operation
    pass

class Ingredient(IngredientBase):
    # Read Operation
    id: int

    class Config:
        getter_dict = MyGetterDict  # use the custom GetterDict class
    
    @root_validator(pre=True)
    def nest_nutritional_values(cls, values):
        values['nutritional_values'] = NutritionalValues(**values)  # enjoy :)
        return values

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
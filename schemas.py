from pydantic import BaseModel, Schema, root_validator, validator, conint
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

# Cooking int schemas
class CookingUnitBase(CamelModel):
    name: str
    short: str
    dimension: str
    factor: float

    class Config:
        orm_mode = True

    @validator('dimension')
    def valid_units_only(cls, v):
        choices = {"mass", "volume"}
        if v not in choices:
            raise ValueError(f"Must be either {' or '.join(choices)}")
        return v

class CookingUnit(CookingUnitBase):
    # Read Operation
    id: int

class CookingUnitCreate(CookingUnitBase):
    # Create Operation
    pass

# Ingredient Schemas
class NutritionalValues(CamelModel):
    calories: conint(gt=-1)
    saturated_fat: conint(gt=-1)
    trans_fat: conint(gt=-1)
    cholesterol: conint(gt=-1)
    sodium: conint(gt=-1)
    carbohydrate: conint(gt=-1)
    sugar: conint(gt=-1)
    protein: conint(gt=-1)

class IngredientBase(CamelModel):
    name: str
    #ingredient_type_id: int = None
    category: str = None
    nutritional_values: Optional[NutritionalValues] = None
    
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
        values["nutritional_values"] = NutritionalValues(**values)  # enjoy :)
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

    class Config:
        orm_mode = True

class IngredientTypeCreate(IngredientTypeBase):
    # Create Operation
    pass

class IngredientType(IngredientTypeBase):
    # Read Operation
    id: int
    ingredients: List[IngredientSubQuery] = []

class IngredientTypeUpdate(IngredientTypeBase):
    # Update Operation
    pass
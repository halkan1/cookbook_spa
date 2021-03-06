from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from database import Base

class CookingUnit(Base):
    __tablename__ = "cooking_unit"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    short = Column(String, unique=True, index=True)
    dimension = Column(String)
    factor = Column(Float)

class Ingredient(Base):
    __tablename__ = "ingredient"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    calories = Column(Float)
    saturated_fat = Column(Float)
    trans_fat = Column(Float)
    cholesterol = Column(Float)
    sodium = Column(Float)
    carbohydrate = Column(Float)
    sugar = Column(Float)
    protein = Column(Float)
    ingredient_type_id = Column(Integer, ForeignKey("ingredient_type.id", ondelete='SET NULL'))
    ingredient_type = relationship("IngredientType", back_populates="ingredients")

    @hybrid_property
    def category(self):
        if self.ingredient_type:
            return self.ingredient_type.name
        return None

class IngredientType(Base):
    __tablename__ = "ingredient_type"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    ingredients = relationship("Ingredient", back_populates="ingredient_type")
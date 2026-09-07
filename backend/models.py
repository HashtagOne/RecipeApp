from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    recipes = db.relationship("Recipe", backref="owner", cascade="all, delete-orphan")

class Recipe(db.Model):
    __tablename__="recipes"
    id = db.Column(db.Integer, primary_key=True)
    user_id= db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    image_url = db.Column(db.String(300), nullable=True)
    prep_time = db.Column(db.Integer, nullable=False)
    cook_time = db.Column(db.Integer, nullable=False)
    servings = db.Column(db.Integer, nullable=False)
    difficulty = db.Column(db.String(30), nullable=False)
    is_public = db.Column(db.Boolean, default=False, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

    recipe_ingredients = db.relationship("RecipeIngredient", backref="recipe", cascade="all, delete-orphan")
    recipe_tags = db.relationship("RecipeTag", backref="recipe", cascade="all, delete-orphan")
    steps = db.relationship("Step", backref="recipe", cascade="all, delete-orphan")

    def to_dict(self): 
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "image_url": self.image_url,
            "prep_time": self.prep_time,
            "cook_time": self.cook_time,
            "servings": self.servings,
            "difficulty": self.difficulty,
            "is_public": self.is_public,
            "created_at": self.created_at.isoformat(),
            "recipe_ingredients": [{"name": ri.ingredient.name,"quantity": ri.quantity, "unit": ri.unit } for ri in self.recipe_ingredients],
            "tags": [rt.tag.name for rt in self.recipe_tags],
            "steps": sorted([{"order_index": s.order_index, "instruction": s.instruction} for s in self.steps], key=lambda x: x["order_index"])
        }

class Ingredient(db.Model):
    __tablename__ = "ingredients"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Tag(db.Model):
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

class RecipeTag(db.Model):
    __tablename__ = "recipe_tags"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id"), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), nullable=False)

    tag = db.relationship("Tag")


class Step(db.Model): 
    __tablename__ = "steps"
    id = db.Column(db.Integer , primary_key=True, nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id"), nullable=False)
    order_index = db.Column(db.Integer, nullable=False)
    instruction = db.Column(db.String(500), nullable=False)

class RecipeIngredient(db.Model):
    __tablename__ = "recipe_ingredients"
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id"), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey("ingredients.id"), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(80), nullable=False)
    order_index = db.Column(db.Integer, nullable=False)

    ingredient = db.relationship("Ingredient")

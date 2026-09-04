from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models import db, Recipe, Ingredient, RecipeTag, Step, RecipeIngredient
from datetime import date

routes_blueprint = Blueprint("routes", __name__)

@routes_blueprint.route("/recipes", methods=["GET"])
@login_required
def get_recipes():

    recipes = Recipe.query.filter_by(user_id=current_user.id).all()
    return jsonify([recipe.to_dict() for recipe in recipes]), 200

@routes_blueprint.route("/recipes/public", methods=["GET"])
def get_publicrecipes():

    recipes = Recipe.query.filter_by(is_public=True).all()
    return jsonify([recipe.to_dict() for recipe in recipes]), 200

@routes_blueprint.route("/recipes", methods=["POST"])
@login_required
def create_recipe():
    data = request.get_json()

    required_fields = ["title", "prep_time", "cook_time", "servings", "difficulty"]

    if not data or any(not data.get(field) for field in required_fields):
        return jsonify({"error": "Missing required fields."}), 400

    recipe = Recipe(
        title = data["title"],
        prep_time = data["prep_time"],
        cook_time = data["cook_time"],
        servings = data["servings"],
        difficulty = data["difficulty"],
        description = data.get("description", ""),
        image_url = data.get("image_url"),
        is_public = data.get("is_public"),
        
        user_id = current_user.id
    )
    db.session.add(recipe)
    db.session.commit()
    return jsonify(recipe.to_dict()), 201
 

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
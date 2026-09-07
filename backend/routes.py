from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models import db, Recipe, Ingredient, RecipeTag, Step, RecipeIngredient, Tag
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
        is_public = data.get("is_public", False),
        user_id = current_user.id
    )
    db.session.add(recipe)
    db.session.flush()

    for index, step_data in enumerate(data.get("steps", [])):
        step = Step(
            recipe_id = recipe.id,
            order_index = index,
            instruction = step_data["instruction"]
        )
        db.session.add(step)

    for tag_name in data.get("tags", []):
        tag = Tag.query.filter_by(name=tag_name.lower()).first()
        if not tag:
            tag = Tag(name=tag_name.lower())
            db.session.add(tag)
            db.session.flush()
        recipe_tag = RecipeTag(recipe_id=recipe.id, tag_id=tag.id)
        db.session.add(recipe_tag)

    for index, ing_data in enumerate(data.get("ingredients", [])):
        ingredient = Ingredient.query.filter_by(name=ing_data["name"].lower()).first()
        if not ingredient:
            ingredient = Ingredient(name=ing_data["name"].lower())
            db.session.add(ingredient)
            db.session.flush()

        recipe_ingredient = RecipeIngredient(
            recipe_id = recipe.id, 
            ingredient_id = ingredient.id, 
            quantity = ing_data["quantity"],
            unit = ing_data["unit"],
            order_index = index

        )
        db.session.add(recipe_ingredient)

    db.session.commit()
    return jsonify(recipe.to_dict()), 201

@routes_blueprint.route("/recipes/<int:id>", methods=["PUT"])
@login_required
def update_recipe(id):
    recipe = db.session.get(Recipe, id)

    if not recipe or recipe.user_id != current_user.id:
        return jsonify({"error": "Recipe not found."}), 404

    data = request.get_json()
    required_fields = ["title", "prep_time", "cook_time", "servings", "difficulty"]
    
    if not data or any(not data.get(field) for field in required_fields):
        return jsonify({"error": "Missing required fields."}), 400

    recipe.title = data["title"]
    recipe.prep_time = data["prep_time"]
    recipe.cook_time = data["cook_time"]
    recipe.servings = data["servings"]
    recipe.difficulty = data["difficulty"]
    recipe.description = data.get("description")
    recipe.image_url = data.get("image_url")
    recipe.is_public = data.get("is_public")

    Step.query.filter_by(recipe_id=recipe.id).delete()
    RecipeIngredient.query.filter_by(recipe_id=recipe.id).delete()
    RecipeTag.query.filter_by(recipe_id=recipe.id).delete()

    for index, step_data in enumerate(data.get("steps", [])):
        step = Step(
            recipe_id = recipe.id,
            order_index = index,
            instruction = step_data["instruction"]
        )
        db.session.add(step)

    for tag_name in data.get("tags", []):
        tag = Tag.query.filter_by(name=tag_name.lower()).first()
        if not tag:
            tag = Tag(name=tag_name.lower())
            db.session.add(tag)
            db.session.flush()
        recipe_tag = RecipeTag(recipe_id=recipe.id, tag_id=tag.id)
        db.session.add(recipe_tag)

    for index, ing_data in enumerate(data.get("ingredients", [])):
        ingredient = Ingredient.query.filter_by(name=ing_data["name"].lower()).first()
        if not ingredient:
            ingredient = Ingredient(name=ing_data["name"].lower())
            db.session.add(ingredient)
            db.session.flush()

        recipe_ingredient = RecipeIngredient(
            recipe_id = recipe.id, 
            ingredient_id = ingredient.id, 
            quantity = ing_data["quantity"],
            unit = ing_data["unit"],
            order_index = index

        )
        db.session.add(recipe_ingredient)

    db.session.commit()
    return jsonify(recipe.to_dict()), 200

@routes_blueprint.route("/recipes/<int:id>", methods=["DELETE"])
@login_required
def delete_recipe(id):
    recipe = db.session.get(Recipe, id)

    if not recipe or recipe.user_id != current_user.id:
        return jsonify({"error": "Recipe not found."}), 404

    db.session.delete(recipe)
    db.session.commit()
    return jsonify({"message": "Recipe deleted."}), 200

@routes_blueprint.route("/recipes/<int:id>/visibility", methods=["PATCH"])
@login_required
def update_visibility(id):
    recipe = db.session.get(Recipe, id)

    if not recipe or recipe.user_id != current_user.id:
        return jsonify({"error": "Recipe not found."}), 404

    recipe.is_public = not recipe.is_public
    db.session.commit()
    return jsonify(recipe.to_dict()), 200

@routes_blueprint.route("/tags", methods=["GET"])
def autocomplete_tag():
    query = request.args.get("q", "")
    tags = Tag.query.filter(Tag.name.ilike(f"%{query}%")).all()
    return jsonify([tag.name for tag in tags]), 200
    

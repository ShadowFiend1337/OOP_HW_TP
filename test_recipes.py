import pytest

from recipes import Ingredient, Recipe, ShoppingList


def ingredients_to_dict(ingredients):
    return {(i.name, i.unit): i.quantity for i in ingredients}


def test_ingredient_creation():
    ingredient = Ingredient("Мука", 500, "г")

    assert ingredient.name == "Мука"
    assert ingredient.quantity == 500.0
    assert ingredient.unit == "г"


def test_ingredient_str():
    ingredient = Ingredient("Мука", 500, "г")

    assert str(ingredient) == "Мука: 500.0 г"


def test_ingredient_eq():
    assert Ingredient("Мука", 500, "г") == Ingredient("Мука", 1000, "г")
    assert Ingredient("Мука", 500, "г") != Ingredient("Сахар", 500, "г")
    assert Ingredient("Мука", 500, "г") != Ingredient("Мука", 500, "кг")


def test_recipe_creation():
    flour = Ingredient("Мука", 500, "г")
    recipe = Recipe("Пицца", [flour])

    assert recipe.title == "Пицца"
    assert recipe.ingredients == [flour]


def test_recipe_add_ingredient_sums_quantity():
    recipe = Recipe("Пицца", [])

    recipe.add_ingredient(Ingredient("Мука", 500, "г"))
    recipe.add_ingredient(Ingredient("Мука", 200, "г"))

    assert len(recipe) == 1
    assert recipe.ingredients[0].quantity == 700.0


def test_recipe_scale():
    recipe = Recipe("Пицца", [Ingredient("Мука", 500, "г")])

    scaled_recipe = recipe.scale(2)

    assert scaled_recipe is not recipe
    assert scaled_recipe.title == "Пицца"
    assert scaled_recipe.ingredients[0].quantity == 1000.0
    assert recipe.ingredients[0].quantity == 500.0


def test_recipe_scale_invalid_ratio():
    recipe = Recipe("Пицца", [Ingredient("Мука", 500, "г")])

    with pytest.raises(ValueError):
        recipe.scale(0)


def test_shopping_list_add_recipe():
    recipe = Recipe("Пицца", [Ingredient("Мука", 500, "г")])
    shopping_list = ShoppingList()

    shopping_list.add_recipe(recipe, 2)

    assert ingredients_to_dict(shopping_list.get_list()) == {
        ("Мука", "г"): 1000.0
    }


def test_shopping_list_get_list_sums_ingredients():
    pizza = Recipe("Пицца", [Ingredient("Мука", 500, "г")])
    pie = Recipe("Пирог", [Ingredient("Мука", 300, "г")])
    shopping_list = ShoppingList()

    shopping_list.add_recipe(pizza, 1)
    shopping_list.add_recipe(pie, 1)

    assert ingredients_to_dict(shopping_list.get_list()) == {
        ("Мука", "г"): 800.0
    }


def test_shopping_list_remove_recipe():
    pizza = Recipe("Пицца", [Ingredient("Мука", 500, "г")])
    shopping_list = ShoppingList()
    shopping_list.add_recipe(pizza, 1)

    shopping_list.remove_recipe("Пицца")

    assert shopping_list.get_list() == []


def test_shopping_list_add_operator():
    first = ShoppingList()
    second = ShoppingList()

    first.add_recipe(Recipe("Пицца", [Ingredient("Мука", 500, "г")]), 1)
    second.add_recipe(Recipe("Суп", [Ingredient("Вода", 1000, "мл")]), 1)

    combined = first + second

    assert ingredients_to_dict(combined.get_list()) == {
        ("Мука", "г"): 500.0,
        ("Вода", "мл"): 1000.0,
    }

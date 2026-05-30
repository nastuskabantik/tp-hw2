import pytest
from recipes import Ingredient, Recipe, ShoppingList, DietaryRecipe

# 2.1. класс Ingredient

def test_ingredient_creation():
    ing = Ingredient("Мука", 500.0, "г")
    assert ing.name == "Мука"
    assert ing.quantity == 500.0
    assert ing.unit == "г"

def test_ingredient_str():
    ing = Ingredient("Мука", 500.0, "г")
    assert str(ing) == "Мука: 500.0 г"

def test_ingredient_eq():
    ing1 = Ingredient("Мука", 500.0, "г")
    ing2 = Ingredient("Мука", 300.0, "г")
    ing3 = Ingredient("Сахар", 500.0, "г")
    ing4 = Ingredient("Мука", 500.0, "кг")

    assert ing1 == ing2
    assert ing1 != ing3
    assert ing1 != ing4

# 2.2. класс Recipe

def test_recipe_creation():
    ing1 = Ingredient("Мука", 500.0, "г")
    recipe = Recipe("Блинчики", [ing1])
    assert recipe.title == "Блинчики"
    assert len(recipe.ingredients) == 1
    assert recipe.ingredients[0].name == "Мука"

def test_recipe_add_ingredient():
    ing1 = Ingredient("Мука", 500.0, "г")
    recipe = Recipe("Блинчики", [ing1])
    
    ing2 = Ingredient("Молоко", 200.0, "мл")
    recipe.add_ingredient(ing2)
    assert len(recipe) == 2
    
    ing3 = Ingredient("Мука", 300.0, "г")
    recipe.add_ingredient(ing3)
    assert len(recipe) == 2
    assert recipe.ingredients[0].quantity == 800.0

def test_recipe_scale():
    ing1 = Ingredient("Мука", 500.0, "г")
    recipe = Recipe("Блинчики", [ing1])
    scaled_recipe = recipe.scale(2)
    assert scaled_recipe is not recipe
    assert scaled_recipe.ingredients[0].quantity == 1000.0
    
    assert recipe.ingredients[0].quantity == 500.0
    
    with pytest.raises(ValueError):
        recipe.scale(0)
    with pytest.raises(ValueError):
        recipe.scale(-1)

def test_recipe_len():
    ing1 = Ingredient("Мука", 500.0, "г")
    ing2 = Ingredient("Молоко", 200.0, "мл")
    recipe = Recipe("Блинчики", [ing1, ing2])
    assert len(recipe) == 2

# 2.3. класс ShoppingList

def test_shopping_list_add_recipe():
    recipe = Recipe("Пицца", [Ingredient("Мука", 400.0, "г")])
    shop_list = ShoppingList()
    
    shop_list.add_recipe(recipe, 2)
    assert len(shop_list._items) == 1
    assert shop_list._items[0][0].quantity == 800.0  # 400 * 2
    
    with pytest.raises(ValueError):
        shop_list.add_recipe(recipe, 0)

def test_shopping_list_remove_recipe():
    recipe1 = Recipe("Пицца", [Ingredient("Мука", 400.0, "г")])
    recipe2 = Recipe("Торт", [Ingredient("Сахар", 200.0, "г")])
    
    shop_list = ShoppingList()
    shop_list.add_recipe(recipe1, 1)
    shop_list.add_recipe(recipe2, 1)
    
    shop_list.remove_recipe("Пицца")
    assert len(shop_list._items) == 1
    assert shop_list._items[0][1] == "Торт"
    
    shop_list.remove_recipe("Салат")  
    assert len(shop_list._items) == 1

def test_shopping_list_get_list():
    recipe1 = Recipe("Пицца", [Ingredient("Мука", 400.0, "г"), Ingredient("Соль", 10.0, "г")])
    recipe2 = Recipe("Хлеб", [Ingredient("Мука", 300.0, "г"), Ingredient("Вода", 200.0, "мл")])
    
    shop_list = ShoppingList()
    shop_list.add_recipe(recipe1, 1)
    shop_list.add_recipe(recipe2, 1)
    
    final_list = shop_list.get_list()
    
    assert len(final_list) == 3
    assert final_list[0].name == "Вода"
    assert final_list[1].name == "Мука"
    assert final_list[1].quantity == 700.0  # 400 + 300
    assert final_list[2].name == "Соль"

def test_shopping_list_add_operator():
    list1 = ShoppingList()
    list1.add_recipe(Recipe("Пицца", [Ingredient("Мука", 400.0, "г")]), 1)
    
    list2 = ShoppingList()
    list2.add_recipe(Recipe("Торт", [Ingredient("Сахар", 200.0, "г")]), 1)
    
    list3 = list1 + list2
    
    assert isinstance(list3, ShoppingList)
    assert len(list3._items) == 2
    
    assert len(list1._items) == 1
    assert len(list2._items) == 1
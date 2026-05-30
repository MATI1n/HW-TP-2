import pytest
from recipes import Ingredient, Recipe, ShoppingList, DietaryRecipe

def test_ingredient_creation():
    ing = Ingredient("Помидоры", 200, "г")
    assert ing.name == "Помидоры"
    assert ing.quantity == 200
    assert ing.unit == "г"

def test_ingredient_str():
    ing = Ingredient("Помидоры", 200, "г")
    assert str(ing) == "Помидоры: 200.0 г"

def test_ingredient_eq():
    ing1 = Ingredient("Помидоры", 200, "г")
    ing2 = Ingredient("Помидоры", 300, "г")
    ing3 = Ingredient("Огурцы", 200, "г")
    ing4 = Ingredient("Помидоры", 200, "кг")
    
    assert ing1 == ing2
    assert ing1 != ing3
    assert ing1 != ing4

def test_shopping_list_add_recipe():
    recipe = Recipe("Салат", [Ingredient("Помидоры", 200, "г")])
    shopping_list = ShoppingList()
    shopping_list.add_recipe(recipe, 2)
    
    assert len(shopping_list._items) == 1

def test_shopping_list_remove_recipe():
    recipe = Recipe("Салат", [Ingredient("Помидоры", 200, "г")])
    shopping_list = ShoppingList()
    shopping_list.add_recipe(recipe, 1)
    
    shopping_list.remove_recipe("Салат")
    assert len(shopping_list._items) == 0
    
    shopping_list.remove_recipe("семечки")

def test_shopping_list_get_list():
    recipe1 = Recipe("Салат", [Ingredient("Помидоры", 200, "г"), Ingredient("Огурцы", 150, "г")])
    recipe2 = Recipe("Странный салат", [Ingredient("Помидоры", 300, "г"), Ingredient("Семечки", 500, "г")])
    
    shopping_list = ShoppingList()
    shopping_list.add_recipe(recipe1, 1)
    shopping_list.add_recipe(recipe2, 1)
    
    final_list = shopping_list.get_list()
    assert len(final_list) == 3
    
    assert final_list[0].name == "Огурцы"
    assert final_list[0].quantity == 150
    
    assert final_list[1].name == "Помидоры"
    assert final_list[1].quantity==500
    
    assert final_list[2].name == "Семечки"
    assert final_list[2].quantity== 500

def test_shopping_list_add_operator():
    recipe1 = Recipe("Пицца", [Ingredient("Помидоры",200,"г")])
    recipe2 = Recipe("Пирог", [Ingredient("Помидоры",300,"г")])
    
    list1 = ShoppingList()
    list1.add_recipe(recipe1,1)
    list2 = ShoppingList()
    list2.add_recipe(recipe2,1)
    
    comb = list1+list2
    assert comb is not list1
    assert comb is not list2
    assert comb.get_list()[0].quantity==500
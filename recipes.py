import copy 

class Ingredient:
    def __init__(self, name: str, quantity: float, unit: str):
        self.name = name
        self._quantity = float(quantity)
        self.unit = unit

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        float_value = float(value)
        if float_value<=0:
            raise ValueError("Количество должно быть положительным")
        self._quantity = float_value

    def __str__(self):
        return f"{self.name}: {self.quantity} {self.unit}"

    def __repr__(self):
        return f"Ingredient('{self.name}', {self.quantity}, '{self.unit}')"

    def __eq__(self, other):
        if not isinstance(other, Ingredient):
            return False
        return self.name==other.name and self.unit==other.unit

class Recipe:
    def __init__(self, title: str, ingredients: list):
        self.title = title
        self.ingredients = []
        for ingredient in ingredients:
            self.add_ingredient(ingredient)

    def add_ingredient(self, ingredient: Ingredient):
        for item in self.ingredients:
            if item == ingredient:
                item.quantity += ingredient.quantity
                return
        self.ingredients.append(Ingredient(ingredient.name, ingredient.quantity, ingredient.unit))

    @staticmethod
    def is_valid_ratio(ratio):
        if not isinstance(ratio, (int, float)):
            return False
        return ratio > 0

    def scale(self, ratio: float):
        if not self.is_valid_ratio(ratio):
            raise ValueError("Коэффициент должен быть положительным")
        new_ingredients = []
        for ingredient in self.ingredients:
            new_ingredients.append(Ingredient(ingredient.name, ingredient.quantity * ratio, ingredient.unit))
        return Recipe(self.title, new_ingredients)
    
    def __len__(self):
        return len(self.ingredients)
    
    def __str__(self):
        lines = [str(ingredient) for ingredient in self.ingredients]
        return f"{self.title}\n"+"\n".join(lines)

class ShoppingList:
    def __init__(self):
        self._items = []

    def add_recipe(self, recipe: Recipe, portions: float):
        if portions <= 0:
            raise ValueError("Количество порций должно быть положительным")
        scaled_recipe = recipe.scale(portions)
        for ingredient in scaled_recipe.ingredients:
            self._items.append((ingredient, recipe.title))

    def remove_recipe(self, title: str):
        self._items = [item for item in self._items if item[1] != title]

    def get_list(self):
        totals = {}
        for ingredient, recipe_title in self._items:
            key = (ingredient.name, ingredient.unit)
            totals[key] = totals.get(key, 0.0) + ingredient.quantity
        
        result_ingredients = []
        for (name, unit), quantity in totals.items():
            result_ingredients.append(Ingredient(name, quantity, unit))
        
        result_ingredients.sort(key=lambda x: x.name)
        return result_ingredients

    def __add__(self, other):
        if not isinstance(other, ShoppingList):
            raise TypeError("Можно объединять только объекты ShoppingList")
        new_list = ShoppingList()
        new_list._items = copy.deepcopy(self._items) + copy.deepcopy(other._items)
        return new_list
    
class DietaryRecipe(Recipe):
    def __init__(self, title: str, diet_type: str, ingredients: list=[]):
        super().__init__(title, ingredients)
        self.diet_type=diet_type

    def scale(self, ratio: float):
        scaled_base = super().scale(ratio)
        return DietaryRecipe(self.title, self.diet_type, scaled_base.ingredients)

    def __str__(self):
        return f"[{self.diet_type}] {super().__str__()}"

def test_recipe_creation():
    items = [Ingredient("Помидоры", 200, "г"), Ingredient("Огурцы", 150, "г")]
    recipe = Recipe("Салат", items)
    assert recipe.title == "Салат"
    assert len(recipe.ingredients) == 2

def test_recipe_add_ingredient():
    recipe = Recipe("Салат", [])
    recipe.add_ingredient(Ingredient("Помидоры", 200, "г"))
    assert len(recipe.ingredients) == 1
    
    recipe.add_ingredient(Ingredient("Помидоры", 300, "г"))
    assert len(recipe.ingredients) == 1
    assert recipe.ingredients[0].quantity == 500

def test_recipe_scale():
    recipe = Recipe("Салат", [Ingredient("Помидоры", 200, "г")])
    scaled = recipe.scale(2)
    
    assert scaled is not recipe
    assert scaled.ingredients[0].quantity==400
    assert recipe.ingredients[0].quantity==200

def test_recipe_len():
    recipe = Recipe("Салат", [Ingredient("Помидоры", 200,"г"), Ingredient("Огурцы",150,"г")])
    assert len(recipe)==2

test_recipe_creation()
test_recipe_add_ingredient()
test_recipe_scale()
test_recipe_len()
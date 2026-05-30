class Ingredient:
    def __init__(self, name: str, quantity: float, unit: str):
        self.name = name
        self.unit = unit
        self.quantity = quantity

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        val = float(value)
        if val <= 0:
            raise ValueError("Количество должно быть положительным")
        self._quantity = val

    def __str__(self):
        return f"{self.name}: {self.quantity} {self.unit}"

    def __repr__(self):
        return f"Ingredient('{self.name}', {self.quantity}, '{self.unit}')"

    def __eq__(self, other):
        if not isinstance(other, Ingredient):
            return False
        return self.name == other.name and self.unit == other.unit
    

class Recipe:
    def __init__(self, title: str, ingredients: list):
        self.title = title
        self.ingredients = ingredients

    def add_ingredient(self, ingredient):
        for item in self.ingredients:
            if item.name == ingredient.name and item.unit == ingredient.unit:
                item.quantity += ingredient.quantity
                return
        self.ingredients.append(ingredient)

    @staticmethod
    def is_valid_ratio(ratio) -> bool:
        return isinstance(ratio, (int, float)) and ratio > 0

    def scale(self, ratio: float):
        if ratio <= 0:
            raise ValueError("Множитель должен быть положительным")
        new_ingredients = [Ingredient(i.name, i.quantity * ratio, i.unit) for i in self.ingredients]
        return Recipe(self.title, new_ingredients)

    def __len__(self):
        return len(self.ingredients)

    def __str__(self):
        ingredients_str = ", ".join(str(i) for i in self.ingredients)
        return f"Рецепт '{self.title}': {ingredients_str}"
    

class ShoppingList:
    def __init__(self):
        self._items = []

    def add_recipe(self, recipe: Recipe, portions: float):
        if portions <= 0:
            raise ValueError("Количество порций должно быть положительным")
        scaled = recipe.scale(portions)
        for ingredient in scaled.ingredients:
            self._items.append((ingredient, recipe.title))

    def remove_recipe(self, title: str):
        self._items = [item for item in self._items if item[1] != title]

    def get_list(self):
        su = {}
        for ingredient, recipe_title in self._items:
            key = (ingredient.name, ingredient.unit)
            if key in su:
                su[key] += ingredient.quantity
            else:
                su[key] = ingredient.quantity
        res = [Ingredient(name, quantity, unit) for (name, unit), quantity in su.items()]
        res.sort(key=lambda x: x.name)
        return res

    def __add__(self, other):
        if not isinstance(other, ShoppingList):
            return NotImplemented
        new_list = ShoppingList()
        new_list._items = self._items.copy() + other._items.copy()
        return new_list
    

class DietaryRecipe(Recipe):
    def __init__(self, title: str, diet_type: str, ingredients=None):
        if ingredients is None:
            ingredients = []
        super().__init__(title, ingredients)
        self.diet_type = diet_type

    def scale(self, ratio: float):
        scaled_recipe_base = super().scale(ratio)
        return DietaryRecipe(self.title, self.diet_type, scaled_recipe_base.ingredients)

    def __str__(self):
        return f"[{self.diet_type}] {super().__str__()}"

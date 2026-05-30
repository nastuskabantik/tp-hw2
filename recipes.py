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
        new_ingredients = [Ingredient(i.name, i.quantity * ratio, i.unit) for i in self.ingredients]
        return Recipe(self.title, new_ingredients)

    def __len__(self):
        return len(self.ingredients)

    def __str__(self):
        ingredients_str = ", ".join(str(i) for i in self.ingredients)
        return f"Рецепт '{self.title}': {ingredients_str}"


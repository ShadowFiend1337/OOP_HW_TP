class Ingredient:
    def __init__(self, name: str, quantity: float, unit: str) -> None:
        self.name = name
        self.quantity = quantity
        self.unit = unit
    
    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, q: float) -> None:
        if q < 0:
            raise ValueError("Количество должно быть положительным")
        self._quantity = float(q)
        
    def __str__(self):
        return f"{self.name}: {self.quantity} {self.unit}"

    def __repr__(self):
        return f"Ingredient({self.name!r}, {self.quantity!r}, {self.unit!r})"

    def __eq__(self, other):
        return self.name == other.name and self.unit == other.unit
    
        


class Recipe:
    def __init__(self, title: str, ingredients: list[Ingredient]) -> None:
        self.title = title
        self.ingredients = ingredients
    
    def add_ingredient(self, ingredient: Ingredient) -> None:
        for i in range(len(self.ingredients)):
            if self.ingredients[i].name == ingredient.name and self.ingredients[i].unit == ingredient.unit:
                self.ingredients[i].quantity += ingredient.quantity
                break
        else:
            self.ingredients.append(ingredient)
    
    @staticmethod
    def is_valid_ratio(ratio):
        return (type(ratio) == float or type(ratio) == int) and ratio > 0
     
    def scale(self, ratio: float):
        if not self.is_valid_ratio(ratio):
            raise ValueError("Коэффициент должен быть положительным")
        new_recipe = Recipe(self.title, [])
        for ingredient in self.ingredients:
            new_ingredient = Ingredient(
                ingredient.name,
                ingredient.quantity * ratio,
                ingredient.unit
            )
            new_recipe.add_ingredient(new_ingredient)
        return new_recipe
    
    def __len__(self):
        return len(self.ingredients)

    def __str__(self):
        result = f"{self.title}\n"
        for ingredient in self.ingredients:
            result += f"- {ingredient}\n"
        return result


class ShoppingList:
    def __init__(self) -> None:
        self._items = []

    def add_recipe(self, recipe: Recipe, portions: float) -> None:
        if portions <= 0:
            raise ValueError("Количество порций должно быть положительным")
        scaled_recipe = recipe.scale(portions)
        for ingredient in scaled_recipe.ingredients:
            self._items.append((ingredient, recipe.title))

    def remove_recipe(self, title: str) -> None:
        self._items = [item for item in self._items if item[1] != title]

    def get_list(self) -> list[Ingredient]:
        ingredients_dict = {}
        for ingredient, recipe_title in self._items:
            key = (ingredient.name, ingredient.unit)
            if key in ingredients_dict:
                ingredients_dict[key] += ingredient.quantity
            else:
                ingredients_dict[key] = ingredient.quantity

        result = []
        for (name, unit), quantity in ingredients_dict.items():
            result.append(Ingredient(name, quantity, unit))
        result.sort(key=lambda ingredient: ingredient.name)

        return result

    def __add__(self, other):
        new_list = ShoppingList()
        new_list._items = self._items.copy() + other._items.copy()
        return new_list


class DietaryRecipe(Recipe):
    def __init__(self, title: str, diet_type: str, ingredients=None) -> None:
        if ingredients is None:
            ingredients = []
        super().__init__(title, ingredients)
        self.diet_type = diet_type

    def scale(self, ratio: float):
        scaled_recipe = super().scale(ratio)
        return DietaryRecipe(
            self.title,
            self.diet_type,
            scaled_recipe.ingredients
        )

    def __str__(self):
        return f"[{self.diet_type}] {super().__str__()}"

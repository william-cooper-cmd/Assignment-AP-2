from MenuItem import MenuItem


class Person:

    def __init__(self, number: int) -> None:
        """Initialises person object"""
        self.number = number
        self.items: list[MenuItem] = []

    def add_item(self, item: MenuItem) -> None:
        """Adds item to person's item list"""
        self.items.append(item)

    def recommend_drink(self, drink_ids: set[int]) -> bool:
        """Return True if a person has not ordered a drink"""
        for item in self.items:
            if item.id in drink_ids:
                return False
        return True

    @property
    def order_total(self) -> float:
        """Returns total cost of all items in this person's order"""
        return sum(item.price for item in self.items)
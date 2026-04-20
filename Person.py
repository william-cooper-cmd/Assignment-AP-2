from MenuItem import MenuItem


class Person:

    def __init__(self, number: int) -> None:
        """Initialises person object"""
        self.number = number
        self.items: list[dict] = []

    def add_item(self, item: MenuItem) -> None:
        """Adds item to person's item list"""
        self.items.append(item)

    def recommend_drink(self, drink_ids: set[int]) -> bool:
        """Check if a drink item is in person's item list"""
        for item in self.items:
            if item['item_number'] in drink_ids:
                return False
        return True

    @property
    def order_total(self) -> float:
        """Returns person's total"""
        return sum([item['price'] for item in self.items])
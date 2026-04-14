class Person:

    def __init__(self, number: int) -> None:
        self.number = number
        self.items: list[dict] = []

    def add_item(self, item: dict) -> None:
        self.items.append(item)

    def recommend_drink(self, drink_ids: set[int]) -> bool:
        for item in self.items:
            if item['item_number'] in drink_ids:
                return False
        return True
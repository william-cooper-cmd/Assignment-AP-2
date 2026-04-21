from MenuItem import MenuItem


class Menu:
    def __init__(self, json_data: dict[str, list[dict]]) -> None:
        """Initialises menu object"""
        self.items: list[MenuItem] = []

        for category, items in json_data.items():
            for item in items:
                self.items.append(
                    MenuItem(
                        id=item["id"],
                        name=item["name"],
                        description=item['description'],
                        price=item["price"],
                        category=category
                    )
                )

    def format_menu(self) -> str:
        """Return all items grouped by category"""
        lines = []
        categories: dict[str, list[MenuItem]] = {}

        # Group items by category
        for item in self.items:
            categories.setdefault(item.category, []).append(item)

        for category, items in categories.items():
            lines.append(f"\n---{category.upper()}---")
            for item in items:
                lines.append(f"{item.id:>3} | {item.name}: {item.decription} - £{item.price:.2f}")

        return "\n".join(lines)

    def get_category_ids(self, category: str) -> set[int]:
        """Return IDs of all items in the category"""
        return {item.id for item in self.items if item.category == category}

    def find_item(self, item_id: int) -> MenuItem | None:
        """Return MenuItem matching given ID"""
        for item in self.items:
            if item.id == item_id:
                return item
        return None

    def get_category_items(self, category: str) -> list[MenuItem]:
        """Return all items in the category"""
        return [item for item in self.items if item.category == category]
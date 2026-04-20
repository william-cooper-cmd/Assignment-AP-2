class Menu:
    def __init__(self, json_data: dict[str, list[dict]]) -> None:
        """Initialises menu object"""
        self.json_data: dict[str, list[dict]] = json_data

    def format_menu(self) -> str:
        """Returns a list of all items, including names, descriptions, and item numbers, sorted by category"""
        lines = []
        for category, items in self.json_data.items():
            lines.append(f"\n---{category.upper()}---")
            for item in items:
                name = item['name']
                number = item['item_number']
                description = item['description']
                lines.append(f"{number:>3} | {name}: {description}")
        return "\n".join(lines)

    def get_category_ids(self, category:str) -> set[int]:
        """Returns ID's of all items in the category"""
        return {d['item_number'] for d in self.json_data[category]}

    def find_item(self, item_number: int) -> dict | None:
        #Converts item number into item dictionary
        for items in self.json_data.values():
            for item in items:
                if item['item_number'] == item_number:
                    return item
        return None

    def get_category_items(self, category: str)-> list[dict]:
        #Returns all items in the category
        return self.json_data[category]
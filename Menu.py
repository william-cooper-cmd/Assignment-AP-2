class Menu:
    def __init__(self, json_data: dict[str, list[dict]]) -> None:
        self.json_data: dict[str, list[dict]] = json_data

    def format_menu(self) -> str:
        lines = []
        for category, items in self.json_data.items():
            lines.append(f"\n---{category.upper()}---")
            for item in items:
                name = item['name']
                number = item['item_number']
                lines.append(f"{number:>3} | {name}")
        return "\n".join(lines)

    def get_category_ids(self, category:str) -> set[int]:
        return {d['item_number'] for d in self.json_data[category]}

    def find_item(self, item_number: int) -> dict | None:
        for items in self.json_data.values():
            for item in items:
                if item['item_number'] == item_number:
                    return item
        return None
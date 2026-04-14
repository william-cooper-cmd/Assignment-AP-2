class Menu:
    def __init__(self, json_data: dict[str, list[dict]]) -> None:
        self.json_data: dict[str, list[dict]] = json_data

    def format_menu(self) -> str:
        lines = []
        for category in self.json_data:
            for item in self.json_data[category]:
                lines.append(f"{item['name']}:{item['item_number']}")
        return "\n".join(lines)

    def get_category_ids(self, category:str) -> set[int]:
        return {d['item_number'] for d in self.json_data[category]}

    def find_item(self, item_number: int) -> dict | None:
        for items in self.json_data.values():
            for item in items:
                if item['item_number'] == item_number:
                    return item
        return None
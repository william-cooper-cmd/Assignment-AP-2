from Table import Table


class Server:

    def __init__(self, server_details: dict) -> None:
        self.tables: list[Table] = []
        self.name: str = server_details['name']
        self.staff_id: str = server_details['staff_id']

    def add_table(self, table: Table) -> None:
        self.tables.append(table)

    def remove_table(self, table: Table) -> bool:
        try:
            self.tables.remove(table)
        except ValueError:
            return False
        return True

    def print_tables(self) -> str:
        lines: list[str] = []
        for table in self.tables:
            lines.append(f"Table Number: {table.number}, Number of people: {table.number_of_people}")
        return "\n".join(lines)
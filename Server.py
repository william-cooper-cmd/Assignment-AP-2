from Table import Table


class Server:

    def __init__(self, server_details: dict) -> None:
        """Initialise server object"""
        self.tables: list[Table] = []
        self.name: str = server_details['name']
        self.staff_id: str = server_details['staff_id']

    def add_table(self, table: Table) -> None:
        """Append table to end of servers list"""
        self.tables.append(table)

    def remove_table(self, table: Table) -> bool:
        """Searches through list of tables and removes the first occurrence"""
        try:
            self.tables.remove(table)
        except ValueError:
            return False
        return True
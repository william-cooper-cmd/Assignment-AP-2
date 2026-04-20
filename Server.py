from Table import Table


class Server:

    def __init__(self, server_details: dict) -> None:
        #Take the server dictionary and extract the name and ID
        self.tables: list[Table] = []
        self.name: str = server_details['name']
        self.staff_id: str = server_details['staff_id']

    def add_table(self, table: Table) -> None:
        #Add the table to the list
        self.tables.append(table)

    def remove_table(self, table: Table) -> bool:
        #Search through the tables list and remove the table
        try:
            self.tables.remove(table)
        except ValueError:
            return False
        return True
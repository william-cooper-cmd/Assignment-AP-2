from Table import Table


class Server:

    def __init__(self, server_details: dict) -> None:
        #Initialise table object
        self.tables: list[Table] = []
        self.name: str = server_details['name']
        self.staff_id: str = server_details['staff_id']

    def add_table(self, table: Table) -> None:
        """Append table to end of servers list"""
        #Add the table to the list
        self.tables.append(table)

    def remove_table(self, table: Table) -> bool:
        """Searches through list of tables and removes the first occurrence"""
        #Search through the tables list and remove the table
        try:
            self.tables.remove(table)
        except ValueError:
            return False
        return True
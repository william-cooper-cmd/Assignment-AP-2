import os
import json

class Server():
    def __init__(self, name):
        self.tables = []
        self.name = name
        self.ID = None

    def add_table(self, table_number, number_people):
        self.tables.append([table_number, number_people])

    def remove_table(self, table_number):
        for table in self.tables:
            if table[0] == table_number:
                self.tables.remove(table)

    def print_tables(self):
        for table in self.tables:
            print(f"Table Number: {table[0]}, Number of people: {table[1]}")



def main():
    if os.path.exists('server.lock'):
      print("Another server is logged in.")
      input("Press any key to exit...")

    else:
        name = input("Please enter your name: ")
        ID = input("Please enter your ID: ")
        try:
            if check_credentials(name, ID):
                server = Server(name)
                print(f"Welcome {server.name}")
                open("server.lock", "w").close()
                input()
                os.remove("server.lock")
        except KeyboardInterrupt:
            os.remove("server.lock")

def check_credentials(name, ID):
    try:
        with open("Servers.json", "r") as f:
            data = json.load(f)
        if name in data:
            if ID == data[name.lower()]:
                return True
            else:
                print("ID does not match server name")
                return False
        else:
            print("Server not found.")
            return False
    except FileNotFoundError:
        print("Servers.json file not found.")
        return False

if __name__ == "__main__":
    main()

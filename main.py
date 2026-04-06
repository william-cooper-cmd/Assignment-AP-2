import os
import json
import random

class Server:
    def __init__(self, name):
        self.tables = []
        self.name = name
        self.staff_id = None

    def add_table(self):
        table = Table()
        print_menu()
        table.add_items()
        self.tables.append(table)


    def remove_table(self):
        table_number = input("Please enter table to remove: ")
        for table in self.tables:
            if table[0] == table_number:
                self.tables.remove(table)
                return True
        return False

    def print_tables(self):
        for table in self.tables:
            print(f"Table Number: {table[0]}, Number of people: {table[1]}")



class Table:

    def __init__(self):
        self.number = int(input("Please enter table number: "))
        self.num_people = int(input("Please enter number of people: "))
        self.people = []

    def create_people(self):
        for number in range(self.num_people):
            person = Person(number)
            self.people.append(person)

    def take_order(self):
        for person in self.people:
            while True:
                choice = input("Please enter your choice: ")
                if not choice:
                    break
                else:
                    try:
                        choice = int(choice)
                    except ValueError:
                        print("Invalid choice.")
                    person.add_item()
            person.recommend_drink()



class Person:
    def __init__(self, number):
        self.name = f"person {number}"
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def recommend_drink(self):
        recommend = False
        for item in self.items:
            if not item.drink:
                recommend = True
        if recommend:
            with open("menu.json", "r") as menu_file:
                menu = json.load(menu_file)
            random.choice(menu["drinks"])




def main():
    if os.path.exists('server.lock'):
      print("Another server is logged in.")
      print("If you're sure another server is not logged in, you can remove server.lock")
      input("Press any key to exit...")

    else:
        name = input("Please enter your name: ")
        staff_id = input("Please enter your staff ID: ")
        try:
            if check_credentials(name, staff_id):
                server = Server(name)
                print(f"Welcome {server.name}")
                open("server.lock", "w").close()
                server_menu(server)
        except KeyboardInterrupt:
            os.remove("server.lock")


def check_credentials(name, staff_id):
    try:
        with open("Servers.json", "r") as f:
            data = json.load(f)
        if name in data:
            if staff_id == data[name.lower()]:
                return True
            else:
                print("staff ID does not match server name")
                return False
        else:
            print("Server not found.")
            return False
    except FileNotFoundError:
        print("Servers.json file not found.")
        return False


def server_menu(server):
    while True:
        print('''1) Add a table
2) Remove a table
3) Print tables
4) Log out''')
        choice = int(input("Enter your choice: "))
        if choice == 1:
            if server.add_table():
                print("Successfully added a table.")
            else:
                print("An error occurred.")
        elif choice == 2:
            if server.remove_table():
                print("Successfully removed a table.")
            else:
                print("An error occurred.")
        elif choice == 3:
            server.print_tables()
        elif choice == 4:
            os.remove("server.lock")
            exit()
        else:
            print("Invalid choice.")


def print_menu():
    with open("menu.json", "r") as menu_file:
        menu = json.load(menu_file)
    for category, items in menu.items():
        print(f"{category}:")
        for item in items:
            print(f"{item['item_number']} - {item['name']}: {item['description']}")


if __name__ == "__main__":
    main()
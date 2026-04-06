from pathlib import Path
import json
import random

class Server:
    def __init__(self, name):
        self.tables = []
        self.name = name

    def add_table(self):
        try:
            table = Table()
        except ValueError:
            print("Failed to create table.")
            return False
        print_menu()
        table.create_people()
        table.take_order()
        self.tables.append(table)
        return True


    def remove_table(self):
        try:
            table_number = int(input("Please enter table to remove: "))
        except ValueError:
            print("Invalid choice.")
            return False
        for table in self.tables:
            if table.number == table_number:
                self.tables.remove(table)
                return True
        return False

    def print_tables(self):
        for table in self.tables:
            print(f"Table Number: {table.number}, Number of people: {table.num_people}")



class Table:

    def __init__(self):
        self.number = int(input("Please enter table number: "))
        self.num_people = int(input("Please enter number of people: "))
        self.people = []

    def create_people(self):
        for number in range(self.num_people):
            person = Person(number+1)
            self.people.append(person)

    def take_order(self):
        for person in self.people:
            print(person.name)
            while True:
                choice = input("Please enter your choice: ")
                if not choice:
                    break
                else:
                    try:
                        choice = int(choice)
                    except ValueError:
                        print("Invalid choice.")
                        continue
                    person.add_item(choice)
            person.recommend_drink()



class Person:
    def __init__(self, number):
        self.name = f"person {number}"
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def recommend_drink(self):
        recommend = True
        drink_ids = {item['item_number'] for item in menu['drinks']}
        if any(num in drink_ids for num in self.items):
            recommend = False
        if recommend:
            recommended = random.choice(menu['drinks'])
            if input(f"Do you want to add {recommended['name']} to your order?").lower() == "yes":
                self.add_item(recommended['item_number'])



def main():
    if lock_file.exists():
      print("Another server is logged in.")
      print("If you're sure another server is not logged in, you can remove server.lock")
      input("Press any key to exit...")

    else:
        name = input("Please enter your name: ")
        staff_id = input("Please enter your staff ID: ")
        if check_credentials(name, staff_id):
            server = Server(name)
            print(f"Welcome {server.name}")
            lock_file.touch()
            try:
                server_menu(server)

            finally:
                if lock_file.exists():
                    lock_file.unlink()


def check_credentials(name, staff_id):
    try:
        with open("Servers.json", "r") as f:
            data = json.load(f)
        if name.lower() in data:
            if staff_id.lower() == data[name.lower()]:
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
        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid choice.")
            continue
        if choice == 1:
            if server.add_table():
                print("Successfully added a table.")
            else:
                print("An error occurred.")
        elif choice == 2:
            if server.remove_table():
                server.print_tables()
                print("Successfully removed a table.")
            else:
                print("An error occurred.")
        elif choice == 3:
            server.print_tables()
        elif choice == 4:
            return
        else:
            print("Invalid choice.")


def print_menu():
    for category, items in menu.items():
        print(f"{category}:")
        for item in items:
            print(f"{item['item_number']} - {item['name']}: {item['description']}")


def load_menu():
    with open("menu.json", "r") as menu_file:
        return json.load(menu_file)

lock_file = Path("server.lock")

try:
    menu = load_menu()
except FileNotFoundError:
    print("Menu file not found.")
    exit(1)

if __name__ == "__main__":
    main()
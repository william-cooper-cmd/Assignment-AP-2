import json
import random
import sys
from pathlib import Path

from Menu import Menu
from Person import Person
from Table import Table
from Server import Server

MENU_FILE = Path("menu.json")
SERVERS_FILE = Path("servers.json")
LOCK_FILE = Path("server.lock")
DRINKS_CATEGORY = "drinks"


def main() -> None:
    menu = load_menu()
    server = authenticate()
    table = setup_table(server)
    print(menu.format_menu())
    take_orders(table, menu)
    print(format_receipt(table, server))


def authenticate() -> Server:
    if acquire_lock():
        sys.exit(f"A server is already logged in. If this is an error delete '{LOCK_FILE}'")
    server = get_server(*get_credentials())
    if not server:
        sys.exit("Name or staff id not found.")
    server = Server(server)
    print(f"Welcome {server.name}")
    return server


def acquire_lock() -> bool:
    try:
        LOCK_FILE.open('x').close()
        return False
    except FileExistsError:
        return True


def get_credentials() -> tuple[str, str]:
    name = input("Enter name: ")
    staff_id = input("Enter staff id: ")
    return name, staff_id


def get_server(name: str, staff_id: str) -> dict | None:
    try:
        with SERVERS_FILE.open() as f:
            server_details = json.load(f)
    except FileNotFoundError:
        sys.exit(f"Error: {SERVERS_FILE} not found.")
    except json.JSONDecodeError as e:
        sys.exit(f"Error: {SERVERS_FILE} is malformed — {e}")
    for server in server_details:
        if server['name'] == name and server['staff_id'] == staff_id:
            return server
    return None


def setup_table(server: Server) -> Table:
    table = Table(*get_table_details())
    server.add_table(table)
    add_people_to_table(table)
    return table


def get_table_details() -> tuple[int, int]:
    number = get_positive_int("Enter table number: ")
    number_of_people = get_positive_int("Enter number of people: ")
    return number, number_of_people


def add_people_to_table(table: Table) -> None:
    for i in range(1, table.number_of_people + 1):
        person = Person(i)
        table.add_person(person)


def take_orders(table: Table, menu: Menu) -> None:
    for person in table.people:
        print(f"person{person.number}:")
        while True:
            item = get_order_items(person, menu)
            if item is None:
                break
            person.add_item(item)
        if person.recommend_drink(menu.get_category_ids(DRINKS_CATEGORY)):
            add_recommended_drink(person, menu)


def get_order_items(person: Person, menu: Menu) -> dict | None:
    while True:
        choice = input("Enter choice: ")
        if choice == "":
            return None
        try:
            choice = int(choice)
        except ValueError:
            print("Must be an integer.")
            continue
        item = menu.find_item(choice)
        if item is None:
            print("Item not found")
            continue
        return item


def add_recommended_drink(person: Person, menu: Menu) -> None:
    recommended_drink = menu.find_item(random.choice(list(menu.get_category_ids(DRINKS_CATEGORY))))
    while True:
        add = input(f"Would you like to add {recommended_drink['name']} to your order? ")
        if add.lower() in ("yes", "y"):
            person.add_item(recommended_drink)
            return
        elif add.lower() in ("no", "n"):
            return
        else:
            print("Must be 'yes' or 'no'")


def get_positive_int(prompt: str) -> int:
    while True:
        value = input(prompt)
        if value.isdigit():
            int_value = int(value)
            if int_value > 0:
                return int_value
        print("Must be a positive integer.")


def format_receipt(table: Table, server: Server) -> str:
    total = 0
    lines = [f'''
        ----------------------------------
            -- The Spectra Pizzeria --
                      Table {table.number}
        ----------------------------------\n''']
    for person in table.people:
        person_total = sum(item['price'] for item in person.items)
        lines.append(f'''        Person {person.number}                    Price\n''')
        for item in person.items:
            lines.append(f"        {item['name']:<26} £{item['price']:>6.2f}\n")
        lines.append(f"        Total:                     £{person_total:>6.2f}\n")
        lines.append("\n")
        total += person_total
    lines.append(f'''        Total for the table:       £{total:>6.2f}\n''')
    lines.append(f'''        Your server is: {server.name}
        Enjoy your meal! Remember to 
        recommend us to friends and family
        ----------------------------------''')
    return "".join(lines)


def load_menu():
    try:
        with open(MENU_FILE, 'r') as file:
            menu = Menu(json.load(file))
    except FileNotFoundError:
        sys.exit(f"Error: {MENU_FILE} not found.")
    except json.JSONDecodeError as error:
        sys.exit(f"Error: {MENU_FILE} is malformed — {error}")
    return menu


if __name__ == "__main__":
    try:
        main()
    finally:
        if LOCK_FILE.exists():
            LOCK_FILE.unlink()

import json
import random
import sys
from pathlib import Path

from Menu import Menu
from Person import Person
from Table import Table
from Server import Server

#File path constants
MENU_FILE = Path("menu.json")
SERVERS_FILE = Path("servers.json")
LOCK_FILE = Path("server.lock")

#Category name constants
DRINKS_CATEGORY = "drinks"


def main() -> None:
    #load the menu, authenticate the server, set up the table, take the order, then print the final receipt
    menu = load_menu()
    server = authenticate()
    table = setup_table(server)
    print(menu.format_menu())
    take_orders(table, menu)
    print(format_receipt(table, server))


def authenticate() -> Server:
    #Check if lock file exists, another server is logged in and exit to prevent multiple logins
    if acquire_lock():
        sys.exit(f"A server is already logged in. If this is an error delete '{LOCK_FILE}'")
    name, staff_id = get_credentials()
    server_details = load_server()
    server = get_server(name, staff_id, server_details)
    if not server:
        sys.exit("Name or staff id not found.")
    server = Server(server)
    print(f"Welcome {server.name}")
    return server


def acquire_lock() -> bool:
    #Open the lock file with exclusive creation mode, it already exists raises FileExistsError
    try:
        LOCK_FILE.open('x').close()
        return False
    except FileExistsError:
        return True


def get_credentials() -> tuple[str, str]:
    #Prompt the user for name and ID
    name = input("Enter name: ").strip()
    staff_id = input("Enter staff id: ").strip()
    return name, staff_id


def load_server() -> list[dict[str, str]]:
    #Load and return the list of servers
    try:
        with SERVERS_FILE.open() as f:
            data = json.load(f)
    except FileNotFoundError:
        sys.exit(f"Error: {SERVERS_FILE} not found.")
    except json.JSONDecodeError as e:
        sys.exit(f"Error: {SERVERS_FILE} is malformed — {e}")
    else:
        return data


def get_server(name: str, staff_id: str, server_details: list[dict]) -> dict | None:
    #Search the sever list for a matching entry for bot name and ID
    for server in server_details:
        if server['name'] == name and server['staff_id'] == staff_id:
            return server
    return None


def setup_table(server: Server) -> Table:
    #Create a table with table number and number of people, create the table object, and add the people
    table = Table(*get_table_details(server))
    server.add_table(table)
    add_people_to_table(table)
    return table


def is_table_number_taken(server: Server, number: int) -> bool:
    #Check if the table number is taken or not
    return any(table.number == number for table in server.tables)


def get_table_number(server: Server) -> int:
    #keep prompting the user until a unique table number is assigned
    while True:
        number = get_positive_int("Enter table number: ")
        if not is_table_number_taken(server, number):
            return number
        print(f"Table {number} is already in use")


def get_table_details(server: Server) -> tuple[int, int]:
    #Prompt the server for table number, and number of people at the table
    number = get_table_number(server)
    number_of_people = get_positive_int("Enter number of people: ")
    return number, number_of_people


def add_people_to_table(table: Table) -> None:
    #Create a Person object for each person at the table
    for i in range(1, table.number_of_people + 1):
        table.add_person(Person(i))


def take_orders(table: Table, menu: Menu) -> None:
    #Loop through each person, get their order, and suggest a drink if they don't have one
    for person in table.people:
        print(f"person{person.number}:")
        while True:
            item = get_order_items(menu)
            if item is None:
                break
            person.add_item(item)
        if person.recommend_drink(menu.get_category_ids(DRINKS_CATEGORY)):
            add_recommended_drink(person, menu)


def get_order_items(menu: Menu) -> dict | None:
    #Prompt for item number and return the matching item
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
    #Select a random drink and ask the server if it should add it to that persons order
    drinks = menu.get_category_items(DRINKS_CATEGORY)
    if not drinks:
        return
    recommended_drink = random.choice(drinks)
    while True:
        add = input(f"Would you like to add {recommended_drink['name']} to your order? ").lower()
        if add in ("yes", "y"):
            person.add_item(recommended_drink)
            return
        elif add in ("no", "n"):
            return
        else:
            print("Must be 'yes' or 'no'")


def get_positive_int(prompt: str) -> int:
    #reprompts until the user enters a positive integer
    while True:
        value = input(prompt)
        if value.isdigit():
            int_value = int(value)
            if int_value > 0:
                return int_value
        print("Must be a positive integer.")


def format_receipt(table: Table, server: Server) -> str:
    #Build the receipt as a list of strings and join at the end
    lines = [f'''
        ----------------------------------
            -- The Spectra Pizzeria --
                      Table {table.number}
        ----------------------------------\n''']
    for person in table.people:
        person_total = person.order_total
        lines.append(f'''        Person {person.number}                    Price\n''')
        for item in person.items:
            lines.append(f"        {item['name']:<26} £{item['price']:>6.2f}\n")
        lines.append(f"        Total:                     £{person_total:>6.2f}\n")
        lines.append("\n")
    total = sum(person.order_total for person in table.people)
    lines.append(f'''        Total for the table:       £{total:>6.2f}\n''')
    lines.append(f'''        Your server is: {server.name}
        Enjoy your meal! Remember to 
        recommend us to friends and family
        ----------------------------------''')
    return "".join(lines)


def load_menu() -> Menu:
    #Load the menu and create a Menu object from it
    try:
        with MENU_FILE.open() as file:
            menu = Menu(json.load(file))
    except FileNotFoundError:
        sys.exit(f"Error: {MENU_FILE} not found.")
    except json.JSONDecodeError as error:
        sys.exit(f"Error: {MENU_FILE} is malformed — {error}")
    else:
        return menu


if __name__ == "__main__":
    try:
        main()
    finally:
        if LOCK_FILE.exists():
            LOCK_FILE.unlink()

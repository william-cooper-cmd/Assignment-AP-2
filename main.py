import json
import random
from pathlib import Path

from Menu import Menu
from MenuItem import MenuItem
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
    #Run the full ordering flow and print the receipt
    menu = load_menu()
    server = authenticate()
    table = setup_table(server)
    print(menu.format_menu())
    take_orders(table, menu)
    print(format_receipt(table, server))


def authenticate() -> Server:
    #Attempts to log server in raises RuntimeError if already logged in or incorrect details
    create_lock()
    name, staff_id = get_credentials()
    server_details = load_server()
    server = get_server(name, staff_id, server_details)
    if not server:
        raise RuntimeError("Name or staff id not found.")
    print(f"Welcome {server.name}")
    return server


def create_lock() -> None:
    #Open lock file raises an error if one already exists
    try:
        LOCK_FILE.open('x').close()
    except FileExistsError:
        raise RuntimeError("Server already logged in")


def get_credentials() -> tuple[str, str]:
    #Prompt for name and ID
    while True:
        name = input("Enter name: ").strip()
        staff_id = input("Enter staff id: ").strip()
        if name == "" or staff_id == "":
            print("Input should not be blank")
            continue
        break
    return name, staff_id


def load_server() -> list[dict[str, str]]:
    #Load and return the list of servers
    try:
        with SERVERS_FILE.open() as f:
            data = json.load(f)
    except FileNotFoundError:
        raise RuntimeError(f"Error: {SERVERS_FILE} not found.")
    except json.JSONDecodeError as error:
        raise RuntimeError(f"Error: {SERVERS_FILE} is malformed — {error}")
    else:
        return data


def get_server(name: str, staff_id: str, server_details: list[dict]) -> Server | None:
    #Find server matching name and staff ID, otherwise return None
    for server in server_details:
        if server['name'] == name and server['staff_id'] == staff_id:
            return Server(server['name'], server['staff_id'])
    return None


def setup_table(server: Server) -> Table:
    #Create a table, register it with server, and assign people to it
    table = Table(*get_table_details(server))
    server.add_table(table)
    add_people_to_table(table)
    return table


def is_table_number_taken(server: Server, number: int) -> bool:
    #Check if table number is already in use
    return any(table.number == number for table in server.tables)


def get_table_number(server: Server) -> int:
    #Prompt until a unique table number is entered
    while True:
        number = get_positive_int("Enter table number: ")
        if not is_table_number_taken(server, number):
            return number
        print(f"Table {number} is already in use")


def get_table_details(server: Server) -> tuple[int, int]:
    #Prompt for table number, and number of people at the table
    number = get_table_number(server)
    number_of_people = get_positive_int("Enter number of people: ")
    return number, number_of_people


def add_people_to_table(table: Table) -> None:
    #Create a Person object for each table seat
    for i in range(1, table.number_of_people + 1):
        table.add_person(Person(i))


def take_orders(table: Table, menu: Menu) -> None:
    #Take each person's order and suggest a drink if applicable
    for person in table.people:
        take_person_order(person, menu)
        maybe_recommend_drink(person, menu)


def take_person_order(person: Person, menu: Menu) -> None:
    #Handle ordering process for a single person
    print(f"\nPerson {person.number}")
    while True:
        item = get_order_items(menu)
        if item is None:
            break
        person.add_item(item)


def get_order_items(menu: Menu) -> MenuItem | None:
    #Prompt for item number and return the matching item
    while True:
        choice = input("Enter choice (blank to finish): ")
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


def maybe_recommend_drink(person: Person, menu: Menu) -> None:
    # Check if a drink should be recommended and offer it
    if person.recommend_drink(menu.get_category_ids(DRINKS_CATEGORY)):
        add_recommended_drink(person, menu)


def add_recommended_drink(person: Person, menu: Menu) -> None:
    #Select a random drink and prompt to add it to the person's order
    drinks = menu.get_category_items(DRINKS_CATEGORY)
    if not drinks:
        print(f"No drinks found in {MENU_FILE}")
        return
    recommended_drink = random.choice(drinks)
    while True:
        add = input(f"Would you like to add {recommended_drink.name} to your order? ").lower()
        if add in ("yes", "y"):
            person.add_item(recommended_drink)
            return
        elif add in ("no", "n"):
            return
        else:
            print("Must be 'yes' or 'no'")


def get_positive_int(prompt: str) -> int:
    #Prompt until a positive integer is entered
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
        except ValueError:
            pass
        print("Must be a positive integer.")


def format_receipt(table: Table, server: Server) -> str:
    #Build the receipt as a list of strings and join at the end
    NAME_WIDTH = 26
    PRICE_WIDTH = 8
    lines = [f'''
        ----------------------------------
            -- The Spectra Pizzeria --
                      Table {table.number}
        ----------------------------------\n''']
    for person in table.people:
        person_total = person.order_total
        lines.append(f"        {'Person ' + str(person.number):<{NAME_WIDTH}} {'Price':>{PRICE_WIDTH}}\n")
        for item in person.items:
            lines.append(f"        {item.name:<{NAME_WIDTH}} £{item.price:>{PRICE_WIDTH}.2f}\n")
        lines.append(f"        {'Total:':<{NAME_WIDTH}} £{person_total:>{PRICE_WIDTH}.2f}\n")
        lines.append("\n")
    total = sum(person.order_total for person in table.people)
    lines.append(f"        {'Total for the table:':<{NAME_WIDTH}} £{total:>{PRICE_WIDTH}.2f}\n")
    lines.append(f'''        Your server is: {server.name}
        Enjoy your meal! Remember to 
        recommend us to friends and family
        ----------------------------------''')
    return "".join(lines)


def load_menu() -> Menu:
    #Load the menu and create a Menu object from it
    try:
        with MENU_FILE.open() as file:
            return Menu(json.load(file))
    except FileNotFoundError:
        raise RuntimeError(f"{MENU_FILE} not found")
    except json.JSONDecodeError as error:
        raise RuntimeError(f"Error: {MENU_FILE} is malformed — {error}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
    finally:
        if LOCK_FILE.exists():
            LOCK_FILE.unlink()

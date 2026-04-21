import pytest

import main
from Menu import Menu
from MenuItem import MenuItem
from Person import Person
from Table import Table
from Server import Server


# -----------------------------
# TEST DATA
# -----------------------------

SAMPLE_SERVERS = [
    {"name": "test", "staff_id": "1"},
    {"name": "test1", "staff_id": "2"}
]

SAMPLE_MENU_DATA = {
    "mains": [
        {"name": "pizza", "id": 1, "price": 10}
    ],
    "drinks": [
        {"name": "Coke", "id": 2, "price": 2.5}
    ]
}


def make_server():
    return Server({"name": "test", "staff_id": "1"})


def make_table_with_orders():
    table = Table(1, 1)
    person = Person(1)
    item = MenuItem(id=1, name="pizza", price=10, category="mains")
    person.add_item(item)
    table.add_person(person)
    return table


# -----------------------------
# get_server
# -----------------------------

def test_get_server_returns_correct():
    result = main.get_server("test", "1", SAMPLE_SERVERS)
    assert result == {"name": "test", "staff_id": "1"}


def test_get_server_wrong_name():
    assert main.get_server("wrong", "1", SAMPLE_SERVERS) is None


def test_get_server_wrong_id():
    assert main.get_server("test", "999", SAMPLE_SERVERS) is None


def test_get_server_both_wrong():
    assert main.get_server("x", "y", SAMPLE_SERVERS) is None


def test_get_server_id_belongs_to_different_user():
    assert main.get_server("test", "2", SAMPLE_SERVERS) is None


def test_get_server_second_user():
    result = main.get_server("test1", "2", SAMPLE_SERVERS)
    assert result == {"name": "test1", "staff_id": "2"}


# -----------------------------
# get_positive_int
# -----------------------------

def test_get_positive_int_valid(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "5")
    assert main.get_positive_int("Enter: ") == 5


def test_get_positive_int_reject_zero(monkeypatch):
    inputs = iter(["0", "3"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert main.get_positive_int("Enter: ") == 3


def test_get_positive_int_reject_negative(monkeypatch):
    inputs = iter(["-1", "2"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert main.get_positive_int("Enter: ") == 2


def test_get_positive_int_reject_text(monkeypatch):
    inputs = iter(["abc", "4"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert main.get_positive_int("Enter: ") == 4


def test_get_positive_int_reject_float(monkeypatch):
    inputs = iter(["1.5", "2"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert main.get_positive_int("Enter: ") == 2


def test_get_positive_int_boundary_one(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "1")
    assert main.get_positive_int("Enter: ") == 1


# -----------------------------
# get_credentials
# -----------------------------

def test_get_credentials(monkeypatch):
    inputs = iter(["test", "1"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert main.get_credentials() == ("test", "1")


def test_get_credentials_strips_whitespace(monkeypatch):
    inputs = iter(["  test  ", "  1  "])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert main.get_credentials() == ("test", "1")


def test_get_credentials_correct_order(monkeypatch):
    inputs = iter(["test", "1"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    name, staff_id = main.get_credentials()
    assert name == "test"
    assert staff_id == "1"


# -----------------------------
# get_table_details
# -----------------------------

def test_get_table_details_returns_correct_types(monkeypatch):
    server = make_server()
    inputs = iter(["1", "2"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    number, people = main.get_table_details(server)
    assert isinstance(number, int)
    assert isinstance(people, int)


def test_get_table_details(monkeypatch):
    server = make_server()
    inputs = iter(["1", "2"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert main.get_table_details(server) == (1, 2)


def test_get_table_details_rejects_invalid_table_number(monkeypatch):
    server = make_server()
    inputs = iter(["abc", "2", "3"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert main.get_table_details(server) == (2, 3)


def test_get_table_details_rejects_zero_table_number(monkeypatch):
    server = make_server()
    inputs = iter(["0", "1", "2"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert main.get_table_details(server) == (1, 2)


def test_get_table_details_rejects_invalid_people_count(monkeypatch):
    server = make_server()
    inputs = iter(["1", "abc", "3"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert main.get_table_details(server) == (1, 3)


def test_get_table_details_rejects_zero_people_count(monkeypatch):
    server = make_server()
    inputs = iter(["1", "0", "2"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert main.get_table_details(server) == (1, 2)


def test_get_table_details_rejects_duplicate_table_number(monkeypatch):
    server = make_server()
    existing_table = Table(1, 2)
    server.add_table(existing_table)
    inputs = iter(["1", "2", "3"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert main.get_table_details(server) == (2, 3)


# -----------------------------
# create_lock
# -----------------------------

def test_create_lock_creates_file(tmp_path, monkeypatch):
    lock = tmp_path / "server.lock"
    monkeypatch.setattr("main.LOCK_FILE", lock)
    main.create_lock()
    assert lock.exists()


def test_create_lock_raises_if_exists(tmp_path, monkeypatch):
    lock = tmp_path / "server.lock"
    lock.touch()
    monkeypatch.setattr("main.LOCK_FILE", lock)
    with pytest.raises(RuntimeError):
        main.create_lock()


# -----------------------------
# add_people_to_table
# -----------------------------

def test_add_people_to_table_correct_count():
    table = Table(1, 3)
    main.add_people_to_table(table)
    assert len(table.people) == 3


def test_add_people_to_table_numbered_from_one():
    table = Table(1, 3)
    main.add_people_to_table(table)
    assert [p.number for p in table.people] == [1, 2, 3]


def test_add_people_to_table_single_person():
    table = Table(1, 1)
    main.add_people_to_table(table)
    assert len(table.people) == 1


def test_add_people_to_table_starts_empty():
    table = Table(1, 2)
    assert table.people == []


# -----------------------------
# get_order_items
# -----------------------------

def test_get_order_items_valid(monkeypatch):
    menu = Menu(SAMPLE_MENU_DATA)
    monkeypatch.setattr("builtins.input", lambda _: "1")
    item = main.get_order_items(menu)
    assert isinstance(item, MenuItem)
    assert item.name == "pizza"


def test_get_order_items_blank(monkeypatch):
    menu = Menu(SAMPLE_MENU_DATA)
    monkeypatch.setattr("builtins.input", lambda _: "")
    assert main.get_order_items(menu) is None


def test_get_order_items_invalid_then_valid(monkeypatch):
    menu = Menu(SAMPLE_MENU_DATA)
    inputs = iter(["99", "1"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    item = main.get_order_items(menu)
    assert item.name == "pizza"


def test_get_order_items_text_then_valid(monkeypatch):
    menu = Menu(SAMPLE_MENU_DATA)
    inputs = iter(["abc", "1"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    item = main.get_order_items(menu)
    assert item.name == "pizza"


# -----------------------------
# add_recommended_drink
# -----------------------------

def test_add_recommended_drink_yes(monkeypatch):
    menu = Menu(SAMPLE_MENU_DATA)
    person = Person(1)
    monkeypatch.setattr("builtins.input", lambda _: "yes")
    monkeypatch.setattr("random.choice", lambda x: MenuItem(id=2, name="Coke", price=2.5, category="drinks"))
    main.add_recommended_drink(person, menu)
    assert any(i.id == 2 for i in person.items)


def test_add_recommended_drink_y(monkeypatch):
    menu = Menu(SAMPLE_MENU_DATA)
    person = Person(1)
    monkeypatch.setattr("builtins.input", lambda _: "y")
    monkeypatch.setattr("random.choice", lambda x: MenuItem(id=2, name="Coke", price=2.5, category="drinks"))
    main.add_recommended_drink(person, menu)
    assert any(i.id == 2 for i in person.items)


def test_add_recommended_drink_no(monkeypatch):
    menu = Menu(SAMPLE_MENU_DATA)
    person = Person(1)
    monkeypatch.setattr("builtins.input", lambda _: "no")
    monkeypatch.setattr("random.choice", lambda x: MenuItem(id=2, name="Coke", price=2.5, category="drinks"))
    main.add_recommended_drink(person, menu)
    assert len(person.items) == 0


def test_add_recommended_drink_n(monkeypatch):
    menu = Menu(SAMPLE_MENU_DATA)
    person = Person(1)
    monkeypatch.setattr("builtins.input", lambda _: "n")
    monkeypatch.setattr("random.choice", lambda x: MenuItem(id=2, name="Coke", price=2.5, category="drinks"))
    main.add_recommended_drink(person, menu)
    assert len(person.items) == 0


def test_add_recommended_drink_invalid_then_yes(monkeypatch):
    menu = Menu(SAMPLE_MENU_DATA)
    person = Person(1)
    inputs = iter(["maybe", "yes"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    monkeypatch.setattr("random.choice", lambda x: MenuItem(id=2, name="Coke", price=2.5, category="drinks"))
    main.add_recommended_drink(person, menu)
    assert any(i.id == 2 for i in person.items)


def test_add_recommended_drink_case_insensitive(monkeypatch):
    menu = Menu(SAMPLE_MENU_DATA)
    person = Person(1)
    monkeypatch.setattr("builtins.input", lambda _: "YES")
    monkeypatch.setattr("random.choice", lambda x: MenuItem(id=2, name="Coke", price=2.5, category="drinks"))
    main.add_recommended_drink(person, menu)
    assert any(i.id == 2 for i in person.items)


# -----------------------------
# format_receipt
# -----------------------------

def test_receipt_contains_table():
    result = main.format_receipt(make_table_with_orders(), make_server())
    assert "Table 1" in result


def test_receipt_contains_server():
    result = main.format_receipt(make_table_with_orders(), make_server())
    assert "test" in result


def test_receipt_contains_item():
    result = main.format_receipt(make_table_with_orders(), make_server())
    assert "pizza" in result
    assert "10.00" in result


def test_receipt_total_present():
    result = main.format_receipt(make_table_with_orders(), make_server())
    assert "Total for the table" in result


def test_receipt_empty_order_shows_zero():
    table = Table(1, 1)
    table.add_person(Person(1))
    result = main.format_receipt(table, make_server())
    assert "0.00" in result


def test_receipt_multiple_people():
    table = Table(1, 2)
    for i in range(1, 3):
        p = Person(i)
        p.add_item(MenuItem(id=1, name="pizza", price=10, category="mains"))
        table.add_person(p)
    result = main.format_receipt(table, make_server())
    assert "Person 1" in result
    assert "Person 2" in result
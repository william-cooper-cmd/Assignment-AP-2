from unittest.mock import patch, mock_open
import json

import main
from Menu import Menu
from Person import Person
from Table import Table
from Server import Server


SAMPLE_SERVERS = json.dumps([
    {"name": "test", "staff_id": "1"},
    {"name": "test1", "staff_id": "2"}
])

SAMPLE_MENU_DATA = {
    "mains": [
        {"name": "pizza", "item_number": 1, "price": 10}
    ],
    "drinks": [
        {"name": "Coke", "item_number": 2, "price": 2.5}
    ]
}

def make_table_with_orders():
    """Creates table with one person and one item"""
    table = Table(1,1)
    person = Person(1)
    person.add_item({"name": "pizza", "item_number": 1, "price": 10})
    table.add_person(person)
    return table

def make_server():
    return Server({"name": "test", "staff_id": "1"})
SAMPLE_SERVERS_LIST = [
    {"name": "test", "staff_id": "1"},
    {"name": "test1", "staff_id": "2"}
]
#Testing get_server
# Testing get_server
def test_get_server_returns_correct_server():
    with patch("main.json.load", return_value=SAMPLE_SERVERS_LIST):
        with patch("pathlib.Path.open"):
            result = main.get_server("test", "1")
            assert result == {"name": "test", "staff_id": "1"}

def test_get_server_returns_none_for_wrong_name():
    with patch("main.json.load", return_value=SAMPLE_SERVERS_LIST):
        with patch("pathlib.Path.open"):
            assert main.get_server("wrong", "1") is None

def test_get_server_returns_none_for_wrong_id():
    with patch("main.json.load", return_value=SAMPLE_SERVERS_LIST):
        with patch("pathlib.Path.open"):
            assert main.get_server("test", "999") is None

def test_get_server_returns_none_for_both_wrong():
    with patch("main.json.load", return_value=SAMPLE_SERVERS_LIST):
        with patch("pathlib.Path.open"):
            assert main.get_server("wrong", "999") is None

def test_get_server_id_belongs_to_different_user():
    with patch("main.json.load", return_value=SAMPLE_SERVERS_LIST):
        with patch("pathlib.Path.open"):
            assert main.get_server("test", "2") is None

def test_get_server_returns_second_user():
    with patch("main.json.load", return_value=SAMPLE_SERVERS_LIST):
        with patch("pathlib.Path.open"):
            result = main.get_server("test1", "2")
            assert result == {"name": "test1", "staff_id": "2"}

#Testing get_positive_int
def test_get_positive_int_valid_input(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "5")
    assert main.get_positive_int("Enter: ") == 5

def test_get_positive_int_rejects_zero_then_accepts(monkeypatch):
    inputs = iter(["0", "3"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert main.get_positive_int("Enter: ") == 3

def test_get_positive_int_rejects_negative_then_accepts(monkeypatch):
    inputs = iter(["-1", "2"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert main.get_positive_int("Enter: ") == 2

def test_get_positive_int_rejects_text_then_accepts(monkeypatch):
    inputs = iter(["abc", "4"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert main.get_positive_int("Enter: ") == 4

def test_get_positive_int_rejects_float_then_accepts(monkeypatch):
    inputs = iter(["1.5", "2"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert main.get_positive_int("Enter: ") == 2

def test_get_positive_int_boundary_value_one(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "1")
    assert main.get_positive_int("Enter: ") == 1


#Test get_credentials
def test_get_credentials_returns_name_and_id(monkeypatch):
    inputs = iter(["test", "1"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert main.get_credentials() == ("test", "1")

def test_get_credentials_correct_order(monkeypatch):
    inputs = iter(["test1", "2"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    name, staff_id = main.get_credentials()
    assert name == "test1"
    assert staff_id == "2"

def test_get_credentials_accepts_empty_strings(monkeypatch):
    inputs = iter(["", ""])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert main.get_credentials() == ("", "")


#Test acquire_lock
def test_acquire_lock_returns_false_when_no_lock(tmp_path, monkeypatch):
    monkeypatch.setattr("main.LOCK_FILE", tmp_path / "server.lock")
    from main import acquire_lock
    assert acquire_lock() is False

def test_acquire_lock_returns_true_when_locked(tmp_path, monkeypatch):
    lock = tmp_path / "server.lock"
    lock.touch()
    monkeypatch.setattr("main.LOCK_FILE", lock)
    from main import acquire_lock
    assert acquire_lock() is True

def test_acquire_lock_creates_file(tmp_path, monkeypatch):
    lock = tmp_path / "server.lock"
    monkeypatch.setattr("main.LOCK_FILE", lock)
    from main import acquire_lock
    acquire_lock()
    assert lock.exists()

def test_acquire_lock_second_call_returns_true(tmp_path, monkeypatch):
    lock = tmp_path / "server.lock"
    monkeypatch.setattr("main.LOCK_FILE", lock)
    from main import acquire_lock
    acquire_lock()
    assert acquire_lock() is True


#Test format_receipt
def test_format_receipt_contains_table_number():
    result = main.format_receipt(make_table_with_orders(), make_server())
    assert "Table 1" in result

def test_format_receipt_contains_server_name():
    result = main.format_receipt(make_table_with_orders(), make_server())
    assert "test" in result

def test_format_receipt_contains_item_name():
    result = main.format_receipt(make_table_with_orders(), make_server())
    assert "pizza" in result

def test_format_receipt_shows_correct_price():
    result = main.format_receipt(make_table_with_orders(), make_server())
    assert "10" in result

def test_format_receipt_multiple_people():
    table = Table(1, 2)
    for i in range(1, 3):
        person = Person(i)
        person.add_item({"name": "pizza", "item_number": 1, "price": 10})
        table.add_person(person)
    result = main.format_receipt(table, make_server())
    assert "Person 1" in result
    assert "Person 2" in result

def test_format_receipt_empty_order_shows_zero_total():
    table = Table(1, 1)
    table.add_person(Person(1))
    result = main.format_receipt(table, make_server())
    assert "0.00" in result


#Test add_people_to_table
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


#Test get_order_items
def test_get_order_items_valid_item_returned(monkeypatch):
    menu = Menu(SAMPLE_MENU_DATA)
    inputs = iter(["1"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    result = main.get_order_items(Person(1), menu)
    assert result == {"name": "pizza", "item_number": 1, "price": 10}

def test_get_order_items_empty_input_returns_none(monkeypatch):
    menu = Menu(SAMPLE_MENU_DATA)
    monkeypatch.setattr("builtins.input", lambda _: "")
    assert main.get_order_items(Person(1), menu) is None

def test_get_order_items_rejects_text_then_accepts(monkeypatch):
    menu = Menu(SAMPLE_MENU_DATA)
    inputs = iter(["1", "1"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    result = main.get_order_items(Person(1), menu)
    assert result == {"name": "pizza", "item_number": 1, "price": 10}

def test_get_order_items_rejects_invalid_number_then_accepts(monkeypatch):
    menu = Menu(SAMPLE_MENU_DATA)
    inputs = iter(["99", "1"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    result = main.get_order_items(Person(1), menu)
    assert result == {"name": "pizza", "item_number": 1, "price": 10}


#Test add_recommend_drink
def test_add_recommended_drink_yes_adds_item(monkeypatch):
    menu = Menu(SAMPLE_MENU_DATA)
    person = Person(1)
    monkeypatch.setattr("builtins.input", lambda _: "yes")
    monkeypatch.setattr("random.choice", lambda x: 2)
    main.add_recommended_drink(person, menu)
    assert any(item['item_number'] == 2 for item in person.items)

def test_add_recommended_drink_y_adds_item(monkeypatch):
    menu = Menu(SAMPLE_MENU_DATA)
    person = Person(1)
    monkeypatch.setattr("builtins.input", lambda _: "y")
    monkeypatch.setattr("random.choice", lambda x: 2)
    main.add_recommended_drink(person, menu)
    assert any(item['item_number'] == 2 for item in person.items)

def test_add_recommended_drink_no_does_not_add(monkeypatch):
    menu = Menu(SAMPLE_MENU_DATA)
    person = Person(1)
    monkeypatch.setattr("builtins.input", lambda _: "no")
    monkeypatch.setattr("random.choice", lambda x: 2)
    main.add_recommended_drink(person, menu)
    assert person.items == []

def test_add_recommended_drink_n_does_not_add(monkeypatch):
    menu = Menu(SAMPLE_MENU_DATA)
    person = Person(1)
    monkeypatch.setattr("builtins.input", lambda _: "n")
    monkeypatch.setattr("random.choice", lambda x: 2)
    main.add_recommended_drink(person, menu)
    assert person.items == []

def test_add_recommended_drink_invalid_then_yes(monkeypatch):
    menu = Menu(SAMPLE_MENU_DATA)
    person = Person(1)
    inputs = iter(["maybe", "yes"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    monkeypatch.setattr("random.choice", lambda x: 2)
    main.add_recommended_drink(person, menu)
    assert any(item['item_number'] == 2 for item in person.items)

def test_add_recommended_drink_case_insensitive(monkeypatch):
    menu = Menu(SAMPLE_MENU_DATA)
    person = Person(1)
    monkeypatch.setattr("builtins.input", lambda _: "YES")
    monkeypatch.setattr("random.choice", lambda x: 2)
    main.add_recommended_drink(person, menu)
    assert any(item['item_number'] == 2 for item in person.items)
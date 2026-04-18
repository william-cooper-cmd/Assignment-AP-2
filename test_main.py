import pytest
from unittest.mock import patch, mock_open
from pathlib import Path
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

#Testing get_server
def test_get_server_returns_correct_server():
    with patch("builtins.open", mock_open(read_data=SAMPLE_SERVERS)):
        result = main.get_server("test", "1")
        assert result == {"name": "test", "staff_id": "1"}

def test_get_server_returns_none_for_wrong_name():
    with patch("builtins.open", mock_open(read_data=SAMPLE_SERVERS)):
        assert main.get_server("wrong", "1") is None

def test_get_server_returns_none_for_wrong_id():
    with patch("builtins.open", mock_open(read_data=SAMPLE_SERVERS)):
        assert main.get_server("test", "999") is None

def test_get_server_returns_none_for_both_wrong():
    with patch("builtins.open", mock_open(read_data=SAMPLE_SERVERS)):
        assert main.get_server("wrong", "999") is None

def test_get_server_id_belongs_to_different_user():
    with patch("builtins.open", mock_open(read_data=SAMPLE_SERVERS)):
        assert main.get_server("test", "2") is None

def test_get_server_returns_second_user():
    with patch("builtins.open", mock_open(read_data=SAMPLE_SERVERS)):
        result = main.get_server("test1", "2")
        assert result == {"name": "test1", "staff_id": "2"}

#Testing get_positive_int
def test_get_positive_int_rejoins_zero_then_Accepts():
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
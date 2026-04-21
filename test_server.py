from Server import Server
from Table import Table

def test_add_table_to_tables():
    server = Server("test", "1")
    table = Table(1,2)
    server.add_table(table)
    assert table in server.tables

def test_remove_table_removes_existing_table():
    server = Server("test", "1")
    table = Table(1,2)
    server.add_table(table)
    result = server.remove_table(table)
    assert result is True
    assert table not in server.tables

def test_remove_tables_returns_false_for_missing_table():
    server = Server("test", "1")
    table = Table(1,2)
    result = server.remove_table(table)
    assert result is False

def test_server_stores_name_and_staff_id():
    server = Server("test", "1")
    assert server.name == "test"
    assert server.staff_id == "1"

def test_server_initialises_with_empty_tables():
    server = Server("test", "1")
    assert server.tables == []
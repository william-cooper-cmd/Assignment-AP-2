from Table import Table
from Person import Person

def test_table_initialises_with_empty_people():
    table = Table(1,2)
    assert table.people == []

def test_add_person_adds_to_people():
    table = Table(1,2)
    person = Person(1)
    table.add_person(person)
    assert person in table.people

def test_table_stores_number_and_amount_of_people():
    table = Table(1,2)
    assert table.number == 1
    assert table.number_of_people == 2
    
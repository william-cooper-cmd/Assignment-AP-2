from Person import Person
from MenuItem import MenuItem

def test_add_item_adds_to_items():
    person = Person(1)
    item = MenuItem(id=2, name="Coke", price=2.50, category="drinks")
    person.add_item(item)
    assert item in person.items

def test_recommended_drink_returns_true_when_no_items():
    person = Person(1)
    assert person.recommend_drink({2}) is True

def test_recommend_drink_returns_false_when_drink():
    person = Person(1)
    person.add_item(MenuItem(id=2, name="Coke", price=2.50, category="drinks"))
    assert person.recommend_drink({2}) is False

def test_recommended_drink_returns_true_when_no_drink():
    person = Person(1)
    person.add_item(MenuItem(id=1, name="Margherita", price=9.99, category="mains"))
    assert person.recommend_drink({2}) is True

def test_order_total_single_item():
    person = Person(1)
    person.add_item(MenuItem(id=1, name="Margherita", price=9.99, category="mains"))
    assert person.order_total == 9.99

def test_order_total_multiple_items():
    person = Person(1)
    person.add_item(MenuItem(id=1, name="Margherita", price=9.99, category="mains"))
    person.add_item(MenuItem(id=2, name="Coke", price=2.50, category="drinks"))
    assert person.order_total == 12.49

def test_order_total_empty_order():
    person = Person(1)
    assert person.order_total == 0
from Person import Person

def test_add_item_adds_to_items():
    person = Person(1)
    item = {
      "item_number": 301,
      "name": "Coca-Cola",
      "description": "Chilled classic Coca-Cola (330ml).",
      "price": 2.50
    }
    person.add_item(item)
    assert item in person.items

def test_recommended_drink_returns_true_when_no_items():
    person = Person(1)
    assert person.recommend_drink({301}) is True

def test_recommend_drink_returns_false_when_drink():
    person = Person(1)
    person.add_item({
      "item_number": 301,
      "name": "Coca-Cola",
      "description": "Chilled classic Coca-Cola (330ml).",
      "price": 2.50
    })
    assert person.recommend_drink({301}) is False

def test_recommended_drink_returns_true_when_no_drink():
    person = Person(1)
    person.add_item({"item_number": 205, "name": "Fries", "description": "Golden crispy fries lightly salted.", "price": 3.50
    })
    assert person.recommend_drink({301}) is True
from Menu import Menu

SAMPLE_MENU = {
    "mains": [
        {"name": "Margherita", "item_number": 1, "price": 9.99}
    ],
    "drinks": [
        {"name": "Coke", "item_number": 2, "price": 2.50}
    ]
}

def test_find_item_returns_correct_item():
    menu = Menu(SAMPLE_MENU)
    result = menu.find_item(1)
    assert result == {"name": "Margherita", "item_number": 1, "price": 9.99}

def test_find_item_returns_none_for_missing_item():
    menu = Menu(SAMPLE_MENU)
    result = menu.find_item(99)
    assert result is None

def test_get_category_id_returns_correct_ids():
    menu = Menu(SAMPLE_MENU)
    assert menu.get_category_ids("drinks") == {2}

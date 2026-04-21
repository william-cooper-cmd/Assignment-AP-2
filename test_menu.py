from Menu import Menu
from MenuItem import MenuItem

SAMPLE_MENU = {
    "mains": [{"id": 1, "name": "Margherita", "price": 9.99, "description": "test"}],
    "drinks": [{"id": 2, "name": "Coke", "price": 2.50, "description": "test"}]
}

def test_find_item_returns_correct_item():
    menu = Menu(SAMPLE_MENU)
    result = menu.find_item(1)
    assert result == MenuItem(id=1, name="Margherita", price=9.99, description="test", category="mains")

def test_find_item_returns_none_for_missing_item():
    menu = Menu(SAMPLE_MENU)
    result = menu.find_item(99)
    assert result is None

def test_get_category_ids_returns_correct_ids():
    menu = Menu(SAMPLE_MENU)
    assert menu.get_category_ids("drinks") == {2}

def test_format_menu_contains_item_names():
    menu = Menu(SAMPLE_MENU)
    result = menu.format_menu()
    assert "Margherita" in result
    assert "Coke" in result

def test_get_category_items_returns_correct_items():
    menu = Menu(SAMPLE_MENU)
    result = menu.get_category_items("drinks")
    assert result == [MenuItem(id=2, name="Coke", price=2.50, description="test", category="drinks")]

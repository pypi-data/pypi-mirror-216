import bien


def test_get_greeting_without_name():
    assert bien.get_greeting() == "Hello, stranger!"


def test_get_greeting_with_name():
    assert bien.get_greeting("Shrek") == "Hello, Shrek!"

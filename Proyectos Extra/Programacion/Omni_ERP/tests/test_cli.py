from dario_app.cli import greet


def test_greet_default():
    assert greet("mundo") == "Hola, mundo!"


def test_greet_name():
    assert greet("Dario") == "Hola, Dario!"

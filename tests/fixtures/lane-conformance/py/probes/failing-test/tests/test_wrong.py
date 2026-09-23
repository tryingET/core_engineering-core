from example_service import add


def test_wrong() -> None:
    assert add(2, 2) == 5

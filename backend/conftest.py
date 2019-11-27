import pytest

from src import create_app

@pytest.fixture
def app():
    app = create_app()
    return app

@pytest.fixture
def client():
    with app.test_client() as c:
        yield c
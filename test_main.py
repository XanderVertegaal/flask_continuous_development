import pytest
from main import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_home_returns_200(client):
    response = client.get('/')
    assert response.status_code == 200


def test_foo_yields_bar(client):
    response = client.get('/foo')
    assert response.data == b'bap'

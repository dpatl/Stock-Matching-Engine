import pytest
from falcon import testing

import src.orders
from src.app import APP


@pytest.fixture
def client():
    return testing.TestClient(APP)

@pytest.fixture
def file():
    return 'C:/Users/deep/documents/Schonfeld/data/ledger.csv'

@pytest.fixture
def trader():
    return 'deep'
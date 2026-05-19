import pytest


@pytest.fixture
def sample_engineer_data():
    return {"engineer_id": "1", "name": "Alice", "region": "US"}

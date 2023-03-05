import pytest

from api.storage.database.settings import PostgresSettings


@pytest.fixture()
def postgres_settings() -> PostgresSettings:
    return PostgresSettings()

import pytest
from starlette.testclient import TestClient

from api.app import App
from api.storage.database.manager import DatabaseManager


@pytest.fixture(scope="function")
def client(app: App) -> TestClient:
    return TestClient(app)


class TestAppEvents:
    def test_startup_event(self, client: TestClient, database_manager: DatabaseManager):
        with client:
            database_manager.connect.assert_called()

    def test_shutdown_event(
        self, client: TestClient, database_manager: DatabaseManager
    ):
        with client:
            pass
        database_manager.disconnect.assert_called()

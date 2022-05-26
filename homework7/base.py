import faker
import pytest

fake = faker.Faker()


class SocketApi:
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, api_client):
        self.api_client = api_client

    @pytest.fixture(scope='function')
    def task_title(self):
        title = fake.lexify(text="???????")
        return title

    @pytest.fixture(scope='function')
    def task(self, task_title):
        resp = self.api_client.add_task(task_title)
        return resp

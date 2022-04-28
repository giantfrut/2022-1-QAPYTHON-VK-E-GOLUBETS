import logging

from base import SocketApi


class TestSocket(SocketApi):

    def test_create_task(self, task, task_title):
        assert task['title'] == task_title
        assert task['done'] is False

    def test_get_description(self, task):
        resp_get = self.api_client.get_description(task['task_id'])
        assert task['description'] == resp_get['description']

    def test_delete_task(self, task):
        resp = self.api_client.delete_task(task['task_id'])
        assert self.api_client.get_description(task['task_id'])['description'] is None
        assert resp == f'Task {task["task_id"]} deleted OK'

    def test_edit_task(self, task):
        resp = self.api_client.edit_task(task['task_id'], not task['done'])
        assert resp['done'] is not task['done']

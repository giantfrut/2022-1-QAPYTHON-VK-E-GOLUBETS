import logging
from _socket import timeout

import settings
import socket
import json


class SocketClient:
    def __init__(self):
        self.target_host = settings.APP_HOST
        self.target_port = int(settings.APP_PORT)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.client.close()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(0.1)
        self.client.connect((self.target_host, self.target_port))

    def read_data(self):
        total_data = []
        try:
            while True:
                # читаем данные из сокета до тех пор пока они там есть
                data = self.client.recv(4096)
                if data:
                    logging.info(f'received data: {data}')
                    total_data.append(data.decode())
                else:
                    break
        except timeout:
            pass

        data = ''.join(total_data).splitlines()
        return json.loads(data[-1])

    def get(self, params):
        request = f'GET {params} HTTP/1.1\r\n' \
                  f'Host:{self.target_host}\r\n\r\n'

        self.connect()
        self.client.send(request.encode())
        return self.read_data()

    def post(self, params, data):
        request = f'POST {params} HTTP/1.1\r\n' \
                  f'Host: {self.target_host}\r\n' \
                  f'Content-Length: {len(data)}\r\n' \
                  f'Content-Type: application/json\r\n\r\n' \
                  f'{data}\r\n\r\n'

        self.connect()
        self.client.send(request.encode())
        return self.read_data()

    def delete(self, params):
        request = f'DELETE {params} HTTP/1.1\r\n' \
                  f'Host:{self.target_host}\r\n\r\n'
        self.connect()
        self.client.send(request.encode())
        return self.read_data()

    def put(self, params, data):
        request = f'PUT {params} HTTP/1.1\r\n' \
                  f'Host: {self.target_host}\r\n' \
                  f'Content-Length: {len(data)}\r\n' \
                  f'Content-Type: application/json\r\n\r\n' \
                  f'{data}\r\n\r\n'

        self.connect()
        self.client.send(request.encode())
        return self.read_data()

    def add_task(self, task_title):
        params = '/add_task'
        data = json.dumps({'title': task_title})
        return self.post(params, data)

    def get_description(self, task_id):
        params = f'/get_task_description_app/{task_id}'
        return self.get(params)

    def delete_task(self, task_id):
        params = f'/tasks_app/{task_id}'
        return self.delete(params)

    def edit_task(self, task_id, status):
        params = f'/edit_task_app/{task_id}'
        data = json.dumps({'done': status})
        return self.put(params, data)

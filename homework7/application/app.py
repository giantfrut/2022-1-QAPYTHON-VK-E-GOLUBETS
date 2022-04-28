#!/usr/bin/env python3.8
import json
import os
import threading
from werkzeug.serving import WSGIRequestHandler

import settings
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)
mock_host = os.environ.get('MOCK_HOST', settings.MOCK_HOST)
mock_port = os.environ.get('MOCK_PORT', settings.MOCK_PORT)

app_data = {}
task_id_seq = 1


@app.route('/add_task', methods=['POST'])
def create_task():
    global task_id_seq
    task_title = json.loads(request.data)['title']
    if task_title not in app_data:
        task_id_seq += 1
        app_data[task_id_seq] = task_title
        # get description from external system
        description = None
        try:
            resp = requests.post(f'http://{mock_host}:{mock_port}/create_task_description/',
                                 json={'task_id': task_id_seq})
            if resp.status_code == 201:
                description = resp.json()
        except Exception as e:
            print(f'Unable to get description from external system 1:\n{e}')

        data = {'task_id': task_id_seq,
                'title': task_title,
                'description': description,
                'done': False,
                }
        return jsonify(data), 200
    else:
        return jsonify(f'Task {task_title} already exist'), 404


@app.route('/get_task_description_app/<int:task_id>', methods=['GET'])
def get_task_description(task_id):
    if task_id in app_data:
        # get description from external system
        description = None
        try:
            resp = requests.get(f'http://{mock_host}:{mock_port}/get_task_description/{task_id}')
            if resp.status_code == 200:
                description = resp.json()
        except Exception as e:
            print(f'Unable to get description from external system 1:\n{e}')

        data = {'task_id': task_id,
                'description': description,
                }
        return jsonify(data), 200
    else:
        return jsonify(f'Task {task_id} dont exist'), 404


@app.route('/tasks_app/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    if task_id in app_data:
        # get delete information from external system
        try:
            resp = requests.delete(f'http://{mock_host}:{mock_port}/tasks/{task_id}')
            if resp.status_code == 204:
                return jsonify(f'Task {task_id} deleted OK'), 200
        except Exception as e:
            print(f'Unable to get delete information from external system 1:\n{e}')
    else:
        return jsonify(f'Task {task_id} dont exist'), 404


@app.route('/edit_task_app/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    if task_id in app_data:
        status = json.loads(request.data)['done']
        done = None
        # get update from information external system
        try:
            response = requests.put(f'http://{mock_host}:{mock_port}/edit_task/{task_id}',
                                    json={'done': status})
            if response.status_code == 200:
                done = response.json()
        except Exception as e:
            print(f'Unable to update task from external system:\n{e}')

        data = {'task_id': task_id_seq,
                'done': done,
                }

        return jsonify(data), 200
    else:
        return jsonify(f'Task {task_id} dont exist'), 404


def shutdown_stub():
    terminate_func = request.environ.get('werkzeug.server.shutdown')
    if terminate_func:
        terminate_func()


@app.route('/shutdown_app', methods=['GET'])
def shutdown_app():
    shutdown_stub()
    return jsonify(f'Ok, exiting'), 200


def run_app():
    server = threading.Thread(target=app.run, kwargs={
        'host': settings.APP_HOST,
        'port': settings.APP_PORT
    })
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    server.start()
    return server

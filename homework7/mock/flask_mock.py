#!/usr/bin/env python3.8
import json
import threading

import faker
from flask import Flask, jsonify, request
from werkzeug.serving import WSGIRequestHandler

import settings

app = Flask(__name__)
DESCRIPTION_DATA = {}
STATUS_DATA = {}
fake = faker.Faker()


@app.route('/create_task_description/', methods=['POST'])
def create_task_description():
    task_id = json.loads(request.data)['task_id']
    if task_id not in DESCRIPTION_DATA:
        DESCRIPTION_DATA[task_id] = fake.lexify(text="??????? ??????? ??????")
        STATUS_DATA[task_id] = False
        return jsonify(DESCRIPTION_DATA[task_id]), 201
    else:
        return jsonify(f'Description for task {task_id} already exists: id: {DESCRIPTION_DATA[task_id]}'), 400


@app.route('/get_task_description/<int:task_id>', methods=['GET'])
def get_task_description(task_id):
    if description := DESCRIPTION_DATA.get(task_id):
        return jsonify(description), 200
    else:
        return jsonify(f'Description for task "{task_id}" not found'), 404


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    if task_id in DESCRIPTION_DATA:
        DESCRIPTION_DATA.pop(task_id)
        STATUS_DATA.pop(task_id)
        return jsonify(f'Task {task_id} deleted OK'), 204
    else:
        return jsonify(f'Task {task_id} dont exist'), 404


@app.route('/edit_task/<int:task_id>', methods=['PUT'])
def edit_task(task_id):
    status = json.loads(request.data)['done']
    if task_id in STATUS_DATA:
        STATUS_DATA[task_id] = status
        return jsonify(STATUS_DATA[task_id]), 200
    else:
        return jsonify(f'Task {task_id} dont exist'), 404


def shutdown_stub():
    terminate_func = request.environ.get('werkzeug.server.shutdown')
    if terminate_func:
        terminate_func()


@app.route('/shutdown_mock', methods=['GET'])
def shutdown_mock():
    shutdown_stub()
    return jsonify(f'Ok, exiting'), 200


def run_mock():
    server = threading.Thread(target=app.run, kwargs={
        'host': settings.MOCK_HOST,
        'port': settings.MOCK_PORT
    })
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    server.start()
    return server

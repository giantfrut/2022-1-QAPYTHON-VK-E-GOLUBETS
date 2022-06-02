#!/usr/bin/env python3.8

from flask import Flask, jsonify, request

app = Flask(__name__)

USERNAME_DATA = {'giantfrut': 1}
vk_id_seq = 1


@app.route('/vk_id/<username>', methods=['GET'])
def get_username(username):
    if vk_id := USERNAME_DATA.get(username):
        return jsonify({"vk_id": str(vk_id)}), 200
    else:
        return jsonify({}), 404


@app.route("/create_vk_id/<username>", methods=['POST'])
def create_vk_id(username):
    global vk_id_seq
    if username not in USERNAME_DATA:
        vk_id_seq += 1
        USERNAME_DATA[username] = vk_id_seq
        return jsonify(f"User {username} get vk_id: {vk_id_seq}"), 201
    else:
        return jsonify("Error. User already have vk_id"), 400


@app.route("/delete_vk_id/<username>", methods=['DELETE'])
def delete_vk_id(username):
    global vk_id_seq
    if username in USERNAME_DATA:
        vk_id_seq -= 1
        USERNAME_DATA.pop(username)
        return jsonify(f"vk_id {username} was deleted"), 204
    else:
        return jsonify("Error. User don't exists"), 400


def shutdown_stub():
    terminate_func = request.environ.get('werkzeug.server.shutdown')
    if terminate_func:
        terminate_func()


@app.route('/shutdown')
def shutdown():
    shutdown_stub()
    return jsonify(f'Ok, mock exiting'), 200



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

from os import environ
from os.path import dirname, join

from dotenv import load_dotenv
from flask import Flask, jsonify, make_response, request, HTTPBasicAuth

BASE_DIR = dirname(dirname(__file__))
load_dotenv(join(BASE_DIR, '.env'))

app = Flask(__name__)
auth = HTTPBasicAuth()

INDICATORS = []
PERIOD = 60
SYMBOLS = []

def login():
    pass


"""
1. Get defined data from XTB
2. Calculate indicators on data
3. Present data and indicators via API for Electron
"""

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]


@app.route('/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

from flask import abort

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201

# update every X period + ping every 9 minutes
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})

@auth.login_required
def get_tasks():
    return jsonify({'tasks': tasks})



@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'Error': 'Not found'}), 404)


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'Error': 'Unauthorized access'}), 403)


if __name__ == '__main__':
    app.run(debug=environ.get("DEBUG"))
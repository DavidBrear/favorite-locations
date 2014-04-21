from flask import request
from app import app
from app.controllers import UserController

@app.route('/users', defaults={'id': None, 'action':None}, methods=['GET', 'POST'])
@app.route('/users/<id>', defaults={'action': None}, methods=['GET', 'POST'])
@app.route('/users/<id>/<action>', methods=['GET', 'POST'])
def users(id, action):
    return UserController().call(request, id, action)

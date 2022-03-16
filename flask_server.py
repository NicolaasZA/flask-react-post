from flask import Flask, redirect, request, json
from src import db
from src.objects import JSONResponse, User, is_not_null

app = Flask(__name__)


def respond_json(data_dict: dict, status=200):
    response = app.response_class(
        response=json.dumps(data_dict),
        status=status,
        mimetype='application/json'
    )
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    # response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


def respond_json_obj(obj: JSONResponse):
    response = app.response_class(
        response=json.dumps({
            'success': obj.success,
            'message': obj.message,
            'data': obj.data
        }),
        status=obj.status,
        mimetype='application/json'
    )
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/', methods=['GET'])
def index():
    return redirect('static/login.html')


@app.route("/signup", methods=['POST', 'OPTIONS'])
def register():
    username: str
    password: str
    typeString: str

    _res = JSONResponse()

    # Read JSON post data
    json_object = request.get_json(silent=True, cache=False)
    if is_not_null(json_object):
        username = json_object['username']
        password = json_object['password']
        typeString = json_object['type']

    if is_not_null(username) and is_not_null(password):
        # Default to programmer account creation.
        if typeString not in ['0', '1']:
            typeString = '0'

        # Check of user klaar geregistreer is.
        _existingUser: User = db.get_user(username, password)

        if _existingUser == None:
            _newUser: User = db.register_user(
                username, password, int(typeString))

            if _newUser != None:
                _res.set_data('user', _newUser.to_json())
                _res.success = True
            else:
                _res.success = False
                _res.message = "Something went wrong during registration."
        else:
            # User bestaan klaar en moet login, nie register nie.
            _res.success = False
            _res.message = "You already have an account. Please login."
    else:
        # Daar is data in die request van die frontend af kort.
        _res.success = False
        _res.message = "Missing required fields"

    return respond_json_obj(_res)


@app.route('/login', methods=['POST', 'OPTIONS'])
def login():
    username: str
    password: str

    _res = JSONResponse()

    # Kry JSON data uit die request
    json_object = request.get_json(silent=True, cache=False)
    if is_not_null(json_object):
        username = json_object['username']
        password = json_object['password']

    # Maak seker 'n username en password is voorsien.
    if is_not_null(username) and is_not_null(password):

        # Replace hierdie met SQL call om te check of die user klaar geregistreer is.
        _user: User = db.get_user(username, password)

        if _user != None:
            # User bestaan, so gee token en email deur vir frontend om te stoor.
            _user.token = db.register_token(_user.id)

            _res.set_data('user', _user.to_json())
            _res.success = True
        else:
            _res.success = False
            _res.message = "Invalid login details. If you do not have an account, kindly register."
    else:
        # Daar is data in die request van die frontend af kort.
        _res.success = False
        _res.message = "Missing required fields"

    return respond_json_obj(_res)


@app.route('/projects', methods=['POST', 'OPTIONS'])
def projects():
    _res = JSONResponse()

    tokenHeader = request.headers['X-TOKEN']

    if db.verify_token_header(tokenHeader):
        _userToken = tokenHeader.split('|')[1]
        _user: User = db.get_user_from_token(_userToken)

        if is_not_null(_user):
            _res.set_data('user', _user.to_json())
            _res.set_data('projects', db.get_available_projects(_user.id))
            _res.success = True
        else:
            _res.success = False
            _res.message = 'Not Authorized. Please login.'
    else:
        _res.success = False
        _res.message = 'Not Authorized. Please login.'

    return respond_json_obj(_res)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

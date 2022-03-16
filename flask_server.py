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
def signup():
    username: str = None
    password: str = None
    typeString: str = None

    responseData = {}
    responseData['success'] = False
    responseData['message'] = ''
    responseData['user'] = None

    # Kry JSON data uit die request
    json_object = request.get_json(silent=True, cache=False)
    if json_object is not None:
        username = json_object['username']
        password = json_object['password']
        typeString = json_object['type']

    # Maak seker 'n username en password is voorsien.
    if username not in ['', None] and password not in ['', None]:
        # Default to programmer account creation.
        if typeString in ['', None] or typeString not in ['0', '1']:
            typeString = '0'

        # Check of user klaar geregistreer is.
        user: User = db.get_user(username, password)

        if user == None:
            # Register user hierso via SQL.
            newUser: User = db.register_user(username, password, int(typeString))

            if newUser != None:
                responseData['user'] = newUser.to_json()
                responseData['success'] = True
                responseData['message'] = ""
            else:
                responseData['user'] = None
                responseData['success'] = False
                responseData['message'] = "Something went wrong during registration."
        else:
            # User bestaan klaar en moet login, nie register nie.
            responseData['success'] = False
            responseData['message'] = "You already have an account. Please login."
    else:
        # Daar is data in die request van die frontend af kort.
        responseData['success'] = False
        responseData['message'] = "Missing required fields"

    return respond_json(responseData)


@app.route('/login', methods=['POST', 'OPTIONS'])
def login():
    responseData = {}
    responseData['success'] = False
    responseData['message'] = ''
    responseData['user'] = None

    username: str = None
    password: str = None

    # Kry JSON data uit die request
    json_object = request.get_json(silent=True, cache=False)
    if json_object is not None:
        username = json_object['username']
        password = json_object['password']

    # Maak seker 'n username en password is voorsien.
    if username not in ['', None] and password not in ['', None]:

        # Replace hierdie met SQL call om te check of die user klaar geregistreer is.
        user: User = db.get_user(username, password)

        if user != None:
            # User bestaan, so gee token en email deur vir frontend om te stoor.
            user.token = db.register_token(user.id)
            responseData['user'] = user.to_json()
            responseData['success'] = True
            responseData['message'] = ""
        else:
            responseData['success'] = False
            responseData['message'] = "Invalid login details. If you do not have an account, kindly register."
    else:
        # Daar is data in die request van die frontend af kort.
        responseData['success'] = False
        responseData['message'] = "Missing required fields"

    return respond_json(responseData)

@app.route('/projects', methods=['POST', 'OPTIONS'])
def projects():
    _res = JSONResponse()
   
    tokenHeader = request.headers['X-TOKEN'] 
    _res.set_data('token', tokenHeader)

    if db.verify_token_header(tokenHeader):
        _userToken = tokenHeader.split('|')[1]
        _user: User = db.get_user_from_token(_userToken)

        if is_not_null(_user):
            _res.set_data('user', _user.to_json())

            _res.set_data('projects', db.get_available_projects(_user.id))
        else:
            _res.success = False
            _res.message = 'Not Authorized. Please login.'
    else:
        _res.success = False
        _res.message = 'Not Authorized. Please login.'
        
    return respond_json_obj(_res)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

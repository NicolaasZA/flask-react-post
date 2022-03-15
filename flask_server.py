from flask import Flask, request, json

from src.user import User, generate_token

app = Flask(__name__)

users: list[User] = []
def get_user(email: str, password: str):
    global users
    for user in users:
        if user.email == email and user.password == password:
            return user
    return None


@app.route("/signup", methods=['POST', 'OPTIONS'])
def signup():
    username: str = None
    password: str = None
    success: bool = False
    message: str = ""

    # Kry JSON data uit die request
    json_object = request.get_json(silent=True, cache=False)
    if json_object is not None:
        username = json_object['username']
        password = json_object['password']

    # Maak seker 'n username en password is voorsien.
    if username not in ['', None] and password not in ['', None]:

        # Replace hierdie met SQL call om te check of die user klaar geregistreer is.
        user = get_user(username, password)

        if user == None:
            # Register user hierso via SQL.
            users.append(User(generate_token(), username, password))

            success = True
            message = "You have been registered. Kindly login."
        else:
            # User bestaan klaar en moet login, nie register nie.
            success = False
            message = "You already have an account. Please login."
    else:
        # Daar is data in die request van die frontend af kort.
        success = False
        message = "Missing required fields"

    # data om terug te stuur na frontend
    response_data = {
        'success': success,
        'message': message
    }

    response = app.response_class(
        response=json.dumps(response_data),
        status=200,
        mimetype='application/json'
    )

    # Add CORS headers
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Origin'] = '*'

    return response


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
        user = get_user(username, password)

        if user != None:
            # User bestaan, so gee token en email deur vir frontend om te stoor.
            responseData['user'] = user.to_json()
            responseData['success'] = True
        else:
            # User bestaan klaar en moet login, nie register nie.
            responseData['success'] = False
            responseData['message'] = "You already have an account. Please login."
    else:
        # Daar is data in die request van die frontend af kort.
        responseData['success'] = False
        responseData['message'] = "Missing required fields"

    response = app.response_class(
        response=json.dumps(responseData),
        status=200,
        mimetype='application/json'
    )

    # Add CORS headers
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Origin'] = '*'

    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
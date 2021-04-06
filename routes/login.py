from app import app, forbidden, internal_server_error, bad_request
from flask import request, jsonify
from routes.auth import authenticate_email


@app.route('/login', methods=['POST'])
def login():
    # Login API, returns dict/403/500
    try:
        try:
            _email = request.form['email']
            _password = request.form['password']
        except Exception as e:
            print(e)
            return bad_request()

        if _email and _password and request.method == 'POST':
            var = authenticate_email(_email, _password)

            if var:
                res = jsonify(var)
                res.status_code = 200
                return res

            # If POST is empty
            else:
                return forbidden()

    except Exception as e:
        print(e)
        return internal_server_error()

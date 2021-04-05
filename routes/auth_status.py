from app import app, forbidden, internal_server_error
from flask import request, jsonify
from routes.auth import authenticate_email_token


@app.route('/auth-status', methods=['POST'])
def auth_status():
    # Auth API, returns True-200/False-403/500
    try:
        _email = request.form['email']
        _token = request.form['token']

        if _email and _token and request.method == 'POST':
            var = authenticate_email_token(_email, _token)

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

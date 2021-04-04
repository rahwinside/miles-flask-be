import pymysql
from firebase_admin import auth

from app import app, forbidden, not_found
from flask import jsonify, request
from routes.auth_status import authenticate
from db_config import mysql

@app.route('/login', methods=['POST'])
def login():
    # Login API, returns status=true/false, isComplete=true/false
    try:
        _uid = request.form['uid']
        _id_token = request.form['idToken']

        if _uid and _id_token and request.method == 'POST':
            var = authenticate(_uid, _id_token)

            if var == "true":
                # Check with db if record is complete
                is_complete = "true"
                sqlQuery = f"SELECT firstName, lastName, areaCode, phoneNumber, postalCode, email, gender, pacemaker, iud, pregnant, allergies, surgeries FROM `users` WHERE uid = '{_uid}'"
                cnx = mysql.connect()
                cursor = cnx.cursor()
                cursor.execute(sqlQuery)
                is_complete = "false"
                for row in cursor:
                    is_complete = "true"
                    for iter in row:
                        if iter is None:
                            is_complete = "false"
                            break

                json_dict = {"auth-status": "true", "isProfileComplete": is_complete}
                res = jsonify(json_dict)
                res.status_code = 200
                return res

            elif var == "invalid-data":
                json_dict = {"auth-status": "invalid-data", "isProfileComplete": "false"}
                res = jsonify(json_dict)
                res.status_code = 403
                return res

            else:
                json_dict = {"auth-status": "false", "isProfileComplete": "false"}
                res = jsonify(json_dict)
                res.status_code = 200
                return res
        # If POST is empty
        else:
            return forbidden()

    except Exception as e:
        print(e)
        return forbidden()
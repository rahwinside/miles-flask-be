import pymysql
from firebase_admin import auth
from app import app, forbidden, not_found, internal_server_error
from flask import jsonify, request
from db_config import mysql


@app.route('/auth-status', methods=['POST'])
# Auth API, returns "true", "false" or 403
def auth_status():
    try:
        _uid = request.form['uid']
        _id_token = request.form['idToken']

        if _uid and _id_token and request.method == 'POST':
            var = authenticate(_uid, _id_token)
            if var == "true":
                # Check with db if record is complete
                sql_query = f"SELECT * FROM `users` WHERE uid = '{_uid}'"
                print(sql_query)
                cnx = mysql.connect()
                cursor = cnx.cursor()
                cursor.execute(sql_query)
                is_complete = "false"
                # Temporary dict to store user info
                for row in cursor:
                    is_complete = "true"
                    for iter in row.values():
                        if iter is None:
                            is_complete = "false"
                            break

                json_dict = {"authStatus": "true", "isProfileComplete": is_complete}

                # Convert int to String for JSON
                if row["pregnant"] == 1:
                    row["pregnant"] = "true"
                else:
                    row["pregnant"] = "false"

                if row["iud"] == 1:
                    row["iud"] = "true"
                else:
                    row["iud"] = "false"

                if row["pacemaker"] == 1:
                    row["pacemaker"] = "true"
                else:
                    row["pacemaker"] = "false"

                # Merge dictionaries
                # json_dict = json_dict | row (PY3.9 only)
                json_dict = {**json_dict, **row}
                # rows = cursor.fetchall()
                res = jsonify(json_dict)
                res.status_code = 200
                return res

            elif var == "invalid-data":
                json_dict = {"authStatus": "invalid-data", "isProfileComplete": "false"}
                res = jsonify(json_dict)
                res.status_code = 403
                return res

            else:
                json_dict = {"authStatus": "false", "isProfileComplete": "false"}
                res = jsonify(json_dict)
                res.status_code = 200
                return res

        # If POST is empty
        else:
            return forbidden()

    except Exception as e:
        print(e)
        return internal_server_error()


# Authentication method for reuse: returns "true", "false", or "invalid-data" || String values, not Boolean
def authenticate(_uid, _id_token):
    try:
        decoded_token = auth.verify_id_token(_id_token)
        uid = decoded_token['uid']
    except Exception as e:
        print(e)
        print("auth:invalid-data")
        return "invalid-data"

    # Check firebase UID with POST UID
    print(decoded_token, uid)
    if uid == _uid:
        print("auth:ok")
        return "true"
    else:
        print("auth:fail")
        return "false"

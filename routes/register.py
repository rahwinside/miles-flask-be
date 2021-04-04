from firebase_admin import auth
from app import app, forbidden
from db_config import mysql
from flask import jsonify, request
from routes.auth_status import authenticate


@app.route('/register', methods=['POST'])
# New user registration API
def register():
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        _uid = request.form['uid']
        _id_token = request.form['idToken']

        if _uid and _id_token and request.method == 'POST':
            var = authenticate(_uid, _id_token)

            if var == "true":
                try:
                    sqlQuery = f"SELECT * FROM users WHERE uid = '{_uid}'"
                    cursor.execute(sqlQuery)
                    account = cursor.fetchone()
                except Exception as e:
                    # print(e)
                    res = jsonify('db-error')
                    # res.status_code = 500              
                    return res

                if account:
                    res = jsonify('exists')
                    # res.status_code = 409               
                    return res
                
                else:
                    # inserting new record into database
                    try:
                        sqlQuery = f"INSERT INTO users(uid) VALUES('{_uid}')"
                        cursor = conn.cursor()
                        cursor.execute(sqlQuery)
                        conn.commit()
                        res = jsonify('success')
                        # res.status_code = 200
                        return res
                    except Exception as e:
                        # print(e)
                        res = jsonify('db-error')
                        # res.status_code = 500               
                        return res


            elif var == "invalid-data":
                # json_dict = {"auth-status": "invalid-data", "isProfileComplete": "false"}
                # res = jsonify(json_dict)
                res = jsonify('fail')
                # res.status_code = 403
                return res

            else:
                # json_dict = {"auth-status": "false", "isProfileComplete": "false"}
                # res = jsonify(json_dict)
                res = jsonify('fail')
                # res.status_code = 200
                return res

        
        # if POST is empty
        else:
            return forbidden()

    except Exception as e:
        # print(e)
        res = jsonify('db-error')
        # res.status_code = 408
        return res
    
    finally:
        cursor.close()
        conn.close()

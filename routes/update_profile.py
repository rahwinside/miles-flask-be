import pymysql
from firebase_admin import auth
from app import app, forbidden
from db_config import mysql
from flask import jsonify, request
from routes.auth_status import authenticate



# Complete profile API. Updates profile and returns 'true' if profile updation is complete. else 'false'
@app.route('/update-profile', methods=['POST'])
def update_profile():

    try:
        _uid = request.form['uid']
        _id_token = request.form['idToken']
        # Checking auth_status
        if _uid and _id_token and request.method == 'POST':
            var = authenticate(_uid, _id_token)

            if var == "true":
                # Getting all info
                _firstName = request.form['firstName']
                _lastName = request.form['lastName']
                _areaCode = request.form['areaCode']
                _phoneNumber = request.form['phone']
                _postalCode = request.form['postalCode']
                _email = request.form['email']
                _gender = request.form['gender']
                _pacemaker = request.form['pacemaker']
                _iud = request.form['iud']
                _pregnant = request.form['pregnant']
                _allergies = request.form['allergies']
                _surgeries = request.form['surgeries']
                _profilePic = request.form['profilePic']
                _city = request.form['city']
                _state = request.form['state']
                _country = request.form['country']
                _address = request.form['address']
                _billingPostalCode = request.form['billingPostalCode']
                _releaseStatement = request.form['releaseStatement']

                if _firstName and _lastName and _areaCode and _phoneNumber and _postalCode and _email and _gender and _pacemaker and _iud and _pregnant and _allergies and _surgeries and _city and _state and _country and _address and _billingPostalCode and _releaseStatement:
                    # Updating record 
                    sqlQuery = f"UPDATE `users` SET `firstName` = '{_firstName}', `lastName` = '{_lastName}', `areaCode` = '{_areaCode}', `phoneNumber` = '{_phoneNumber}', `postalCode` = '{_postalCode}', `billingPostalCode` = '{_billingPostalCode}', `email` = '{_email}', `gender` = '{_gender}', `pacemaker` = '{_pacemaker}', `iud` = '{_iud}', `pregnant` = '{_pregnant}', `allergies` = '{_allergies}', `surgeries` = '{_surgeries}', `profilePic` = '{_profilePic}',`city` = '{_city}',`state` = '{_state}', `country` = '{_country}', `address` = '{_address}', `releaseStatement` = '{_releaseStatement}' WHERE `uid` = '{_uid}'"
                    conn = mysql.connect()
                    cursor = conn.cursor()
                    cursor.execute(sqlQuery)
                    conn.commit()
                    res = jsonify('success')
                    res.status_code = 200
                    cursor.close()
                    conn.close()
                    return res
                else:
                    res = jsonify('invaild-request')
                    res.status_code = 200
                    return res

            else:
                res = jsonify('auth-error')
                res.status_code = 403
                return res

        else:
            return forbidden()

    except Exception as e:
        print(e)
        return forbidden()

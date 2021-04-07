from app import app, forbidden, internal_server_error, bad_request
from flask import request, jsonify

from db_config import mysql
from routes.auth import authenticate_email_token


@app.route('/cancel-ride', methods=['POST'])
def cancel_ride():
    try:
        try:
            _email = request.form['email']
            _token = request.form['token']
            _ride_id = request.form['rideID']
            _bike_id = request.form['bikeID']
        except Exception as e:
            print(e)
            return bad_request()

        if _email and _token and _ride_id and _bike_id and request.method == 'POST':
            var = authenticate_email_token(_email, _token)

            if var:
                # Update ride status to canceled
                sql = f"UPDATE rides SET status = 'canceled', endTimeStamp = CURRENT_TIMESTAMP WHERE rideID = {_ride_id}"
                cnx = mysql.connect()
                cursor = cnx.cursor()
                cursor.execute(sql)
                cursor.close()
                cnx.commit()

                # Remove reservation from  bikes
                sql = f"UPDATE bikes SET status = 'free', reserveTimeStamp = NULL, currentRideID = NULL WHERE bikeID = {_bike_id} "
                cursor = cnx.cursor()
                cursor.execute(sql)
                cursor.close()
                cnx.commit()

                res = jsonify("canceled")
                res.status_code = 200
                return res

            else:
                return forbidden()

    except Exception as e:
        print(e)
        return internal_server_error()

from app import app, forbidden, internal_server_error, bad_request
from flask import request, jsonify

from db_config import mysql
from routes.auth import authenticate_email_token


@app.route('/get-bikes', methods=['POST'])
def get_bikes():
    try:
        try:
            _email = request.form['email']
            _token = request.form['token']
        except Exception as e:
            print(e)
            return bad_request()

        if _email and _token and request.method == 'POST':
            var = authenticate_email_token(_email, _token)

            if var:
                sql = f"SELECT bikes.bikeID, bikes.currentStationID, bikes.status, stations.stationName FROM bikes, " \
                      f"stations, users WHERE users.email = '{_email}' AND  bikes.currentStationID =  " \
                      f"stations.stationID AND stations.domain = users.domain "
                cnx = mysql.connect()
                cursor = cnx.cursor()
                cursor.execute(sql)
                bike_list = []
                for row in cursor:
                    bike_list.append(row)

                res = jsonify(bike_list)
                res.status_code = 200
                return res

            # If POST is empty
            else:
                return forbidden()

    except Exception as e:
        print(e)
        return internal_server_error()


@app.route('/get-avail-bikes', methods=['POST'])
def get_bikes_avail_count():
    try:
        try:
            _email = request.form['email']
            _token = request.form['token']
        except Exception as e:
            print(e)
            return bad_request()

        if _email and _token and request.method == 'POST':
            var = authenticate_email_token(_email, _token)

            if var:
                sql = f"SELECT stations.stationName, stations.stationID, count(bikes.bikeID) AS available FROM bikes, " \
                      f"stations, users WHERE users.email = '{_email}' AND bikes.currentStationID = " \
                      f"stations.stationID AND stations.domain = users.domain AND bikes.status = 'free' GROUP BY " \
                      f"stations.stationName, stations.stationID "
                cnx = mysql.connect()
                cursor = cnx.cursor()
                cursor.execute(sql)
                bike_list = []
                for row in cursor:
                    bike_list.append(row)

                res = jsonify(bike_list)
                res.status_code = 200
                return res

            # If POST is empty
            else:
                return forbidden()

    except Exception as e:
        print(e)
        return internal_server_error()

from app import app, forbidden, internal_server_error, bad_request
from flask import request, jsonify

from db_config import mysql
from routes.auth import authenticate_email_token


@app.route('/reserve-bike', methods=['POST'])
def reserve_bike():
    try:
        try:
            _email = request.form['email']
            _token = request.form['token']
            _station_id = request.form['stationID']
        except Exception as e:
            print(e)
            return bad_request()

        if _email and _token and _station_id and request.method == 'POST':
            var = authenticate_email_token(_email, _token)

            if var:
                # Close all reserved rides older than 5 minutes
                sql = f"UPDATE rides SET status = 'canceled' WHERE reserveTimeStamp < (NOW() - INTERVAL 5 MINUTE) AND " \
                      f"status = 'reserved' "
                cnx = mysql.connect()
                cursor = cnx.cursor()
                cursor.execute(sql)
                cursor.close()
                cnx.commit()

                # Remove reservations from reserved bikes older than 5 minutes
                sql = f"UPDATE bikes SET status = 'free', reserveTimeStamp = NULL, currentRideID = NULL WHERE " \
                      f"reserveTimeStamp < (NOW() - INTERVAL 5 MINUTE) AND status = 'reserved' "
                cursor = cnx.cursor()
                cursor.execute(sql)
                cursor.close()
                cnx.commit()

                # Find an available bike
                # sql = f"SELECT bikeID from bikes INNER JOIN (SELECT min(lastRideID) minLastRideID FROM bikes WHERE " \
                #       f"currentStationID = {_station_id}  AND status = 'free') minTable ON bikes.lastRideID = " \
                #       f"minTable.minLastRideID WHERE lastRideID = minLastRideID AND currentStationID = {_station_id} " \
                #       f"AND status = 'free' "

                sql = f"SELECT bikeID from bikes WHERE (lastRideID = (SELECT min(lastRideID) FROM bikes WHERE " \
                      f"currentStationID = {_station_id} AND status = 'free') OR lastRideID IS NULL) AND " \
                      f"currentStationID = {_station_id} AND status = 'free' "
                cursor = cnx.cursor()
                cursor.execute(sql)
                for first_bike in cursor:
                    bike_id = first_bike["bikeID"]
                    print("BikeID: " + str(bike_id))
                    break
                cursor.close()

                # If query returns no bikes
                try:
                    if bike_id is None:
                        raise Exception("no-avail-bikes")
                except Exception as e:
                    res = jsonify("no-available-bikes")
                    res.status_code = 200
                    return res

                # Create ride with bikeID
                sql = f"INSERT INTO rides (emailID, bikeID, startStationID) VALUES ('{_email}', {bike_id}, {_station_id})"
                cursor = cnx.cursor()
                cursor.execute(sql)
                current_ride_id = cursor.lastrowid
                print("RideID: " + str(current_ride_id))
                cursor.close()
                cnx.commit()

                # Update bike with rideID and status
                sql = f"UPDATE bikes SET currentRideID = {current_ride_id}, status = 'reserved', reserveTimeStamp = " \
                      f"CURRENT_TIMESTAMP WHERE bikeID = {bike_id} "
                cursor = cnx.cursor()
                cursor.execute(sql)
                cursor.close()
                cnx.commit()

                # Get bike specifications and ride information
                sql = f"SELECT bikeID, currentRideID, homeStationID, currentStationID, status, reserveTimeStamp, " \
                      f"make, model, year FROM bikes WHERE bikeID = {bike_id} "
                cursor = cnx.cursor()
                cursor.execute(sql)
                for ride_info in cursor:
                    break
                cursor.close()

                res = jsonify(ride_info)
                res.status_code = 200
                return res
            else:
                return forbidden()

    except Exception as e:
        print(e)
        return internal_server_error()

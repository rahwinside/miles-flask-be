from db_config import mysql


def authenticate_email(email, password):
    sql = f"SELECT users.userID, users.emailID, users.fullName, users.token, users.domain, users.rollNo, users.department, users.bloodType, users.phone, users.emergencyContact, users.emergencyContactName, users.emergencyContactRelation, users.lastSignInTimeStamp, users.signUpTimeStamp, domains.organizationName, domains.email, domains.phone, domains.address, FROM users, domains WHERE users.domain = domains.domain AND email = '{email}' AND password = '{password}'"
    cnx = mysql.connect()
    cursor = cnx.cursor()
    cursor.execute(sql)
    for row in cursor:
        for iter in row:
            if iter is None:
                is_complete = "false"
                break

    json_dict = {"auth-status": "true", "isProfileComplete": is_complete}
    res = jsonify(json_dict)
    res.status_code = 200
    return res
from db_config import mysql
import hashlib


def authenticate_email(email, password):
    password = hashlib.sha512(password).digest()
    sql = f"SELECT users.userID, users.emailID, users.fullName, users.token, users.domain, users.rollNo, users.department, users.bloodType, users.phone, users.emergencyContact, users.emergencyContactName, users.emergencyContactRelation, users.lastSignInTimeStamp, users.signUpTimeStamp, domains.organizationName, domains.email, domains.phone, domains.address, FROM users, domains WHERE users.domain = domains.domain AND email = '{email}' AND password = '{password}'"
    cnx = mysql.connect()
    cursor = cnx.cursor()
    cursor.execute(sql)
    for row in cursor:
        return row
    return False

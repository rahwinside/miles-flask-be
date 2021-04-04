from db_config import mysql
from random_string import random_string
import hashlib


def authenticate_email(email, password):
    try:
        password = hashlib.sha512(str(password).encode("utf-8")).hexdigest()
        sql = f"SELECT users.userID, users.email, users.fullName, users.token, users.domain, users.rollNo, users.department, users.bloodType, users.phone, users.emergencyContact, users.emergencyContactName, users.emergencyContactRelation, users.lastSignInTimeStamp, users.signUpTimeStamp, domains.organizationName, domains.email, domains.phone, domains.address FROM users, domains WHERE users.domain = domains.domain AND users.email = '{email}' AND users.password = '{password}'"
        cnx = mysql.connect()
        cursor = cnx.cursor()
        cursor.execute(sql)
        for row in cursor:
            cursor.close()
            token = random_string(100)
            sql = f"UPDATE users set token = '{token}' WHERE email = '{email}'"
            cursor = cnx.cursor()
            cursor.execute(sql)
            cnx.commit()
            cnx.close()

            if cursor.rowcount == 1:
                row["token"] = token
                return row
            else:
                return False
        return False
    except Exception as e:
        print(e)
        return False

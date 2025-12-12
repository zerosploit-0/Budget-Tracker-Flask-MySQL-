import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Root1234!",
        database="budget_tracker"

    )
    return connection

# MySQL Root user und pw
# user: root
# pw: Root1234!
# Temp pw testing: IabkOVlT@g76eA_IKzT.fm
#prod =6-.MWH7u3fo0wy1ws_KRV
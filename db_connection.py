 
import mysql.connector

def get_db_connection():
    config = {
        "user": "root",         
        "password": "Sanidhya@28", 
        "host": "localhost",         
        "database": "qc_lab"  
    }
    return mysql.connector.connect(**config)


 
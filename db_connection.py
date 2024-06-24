 
import mysql.connector

def get_db_connection():
    config = {
        "user": "lax",         
        "password": "Sanidhya@28", 
        "host": "qc-lab.mysql.database.azure.com",         
        "database": "qc_lab"  
    }
    return mysql.connector.connect(**config)


 
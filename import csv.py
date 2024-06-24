import csv
import mysql.connector

db_config = {
    'user': 'root',
    'password': 'Sanidhya@28',
    'host': 'Localhost',
    'database': 'test'
}
 
 
 
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()
def convert_empty_to_none(row):
    return [None if field == '' else field for field in row]

 
with open("O:\internship\SQL Data\AnalysisReg.csv", mode='r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip the header row

    # Insert each row into the table
    for row in csv_reader:
        row = convert_empty_to_none(row)
        cursor.execute(
            "INSERT INTO analysisreg (AnlysID, SampleID, LabID, TestType, UserID, Material, M_C, O_C, FFA, FM, S_S, PROTIEN, CLR, MIV, EO, IV, SV, Date_Time_Stmp, Remarks) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            row
        )

# Commit the transaction
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()


cursor.close()
conn.close()


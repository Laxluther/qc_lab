
from datetime import datetime
from db_connection import get_db_connection
 
from datetime import datetime


class DatabaseOperations:
    def __init__(self, get_db_connection):
        self.get_db_connection = get_db_connection

    def get_materials(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT PRODUCT FROM l_tst")
        materials = [row[0] for row in cursor.fetchall()]
        conn.close()
        return materials

    def check_user_credentials(self, userid, password):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM L_Usr WHERE USER_ID = %s AND PASSWORD = %s", (userid, password))
        user = cursor.fetchone()
        conn.close()
        return user

    def get_user_name(self, user_id):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT USER FROM L_Usr WHERE USER_ID = %s", (user_id,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None

    def get_sample_points(self, material):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT smplPtID
            FROM L_smplptmatrix
            WHERE PRODUCT = %s
        """, (material,))
        sample_points = [row[0] for row in cursor.fetchall()]
        conn.close()
        return sample_points

    def get_lab_name(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT LAB_ID FROM l_lab")
        lab_name = [row[0] for row in cursor.fetchall()]
        conn.close()
        return lab_name 
    def get_lab(self,labID):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT LABORATORY FROM l_lab WHERE LAB_ID = %s",(labID,))
        lab =  cursor.fetchone()
        conn.close()
        return lab

    def get_sampler_id(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT SAMPLER_ID FROM l_smplr ")
        sampler_ids = [row[0] for row in cursor.fetchall()]
        conn.close()
        return sampler_ids
    def get_sampler(self,samplerID):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT SAMPLER FROM l_smplr WHERE SAMPLER_ID = %s",(samplerID,))
        sampler =  cursor.fetchone()
        conn.close()
        return sampler
    def get_test_req(self, material):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT PARAMETER_1, PARAMETER_2, PARAMETER_3, PARAMETER_4, PARAMETER_5, PARAMETER_6
            FROM l_tst 
            WHERE PRODUCT = %s
        """, (material,))
        test_req = cursor.fetchone()
        conn.close()
        return test_req
    
    def get_std_test(self, material,sampleType):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT PARAMETER_1, PARAMETER_2, PARAMETER_3, PARAMETER_4, PARAMETER_5, PARAMETER_6
            FROM l_test 
            WHERE PRODUCT = %s AND SampleType = %s
        """, (material,sampleType))
        test_std = cursor.fetchone()
        conn.close()
        return test_std

    def get_last_sample_id(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(CAST(SampleID AS UNSIGNED)) FROM samplereg")
        result = cursor.fetchone()
        last_sample_id = result[0] if result[0] is not None else 0
        conn.close()
        return last_sample_id

    def get_analysis_id(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT MAX(CAST(AnlysID AS UNSIGNED)) FROM AnalysisReg")
        result = cursor.fetchone()
        analysis_id = result[0] if result is not None else 0
        conn.close()
        return analysis_id

    def get_limits(self, material):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
        "SELECT Value, Min, Max FROM L_TstCd WHERE PRODUCT = %s", (material,))
        limits = cursor.fetchall()
        conn.close()
        return [list(row) for row in limits]


    def unanalys_sample_id(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT SampleID 
            FROM samplereg 
            WHERE SampleID NOT IN (SELECT SampleID FROM analysisreg) and SampleID > 1000 
        """)
        sample_ids = [row[0] for row in cursor.fetchall()]
        conn.close()
        return sample_ids

    def last_sample_id_ana(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT SampleID 
            FROM analysisreg 
            ORDER BY Date_Time_Stmp DESC
            LIMIT 10   
        """)
        sample_ids = [row[0] for row in cursor.fetchall()]
        conn.close()
        return sample_ids

    def get_data(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM analysisreg 
                       WHERE  DATE(DATE_Time_Stmp) = CURDATE()
                       ORDER BY SampleID DESC """)
        data = cursor.fetchall()
        conn.close()
         
        return data
    def get_data_sam(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM samplereg 
                       WHERE  DATE(Date_Time_Stmp) = CURDATE()
                       ORDER BY SampleID DESC """)
        data = cursor.fetchall()
        conn.close()
         
        return data


    def get_sample_id(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT SampleID 
            FROM samplereg ORDER BY SampleID DESC 
        """)
        sample_ids = [row[0] for row in cursor.fetchall()]
        conn.close()
        return sample_ids

    def get_values(self, sample_id):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Material, PARAMETER_1, PARAMETER_2, PARAMETER_3, PARAMETER_4, PARAMETER_5, PARAMETER_6
            FROM SampleReg 
            WHERE SampleID = %s
        """, (sample_id,))
        val = cursor.fetchone()
        conn.close()
        return val

     
 

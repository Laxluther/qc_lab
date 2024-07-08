from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from database_operations import DatabaseOperations
from datetime import datetime
from db_connection import get_db_connection
import mysql.connector
from dash_app import DailyReportDashboard
from dash_app_monthly import DailyReportDashboardMonthly
from dispatch_report import DispatchDashboard
from comb import CombinedDashboard
from monthlyDispatch import DispatchMonthly
app = Flask(__name__)
app.secret_key = '28'

db_ops = DatabaseOperations(get_db_connection)
conn = get_db_connection()


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userid = request.form['userid']
        password = request.form['password']
        user = db_ops.check_user_credentials(userid, password)
        if user:
            session['user'] = userid
            return redirect(url_for('home'))
        else:
            error = "Invalid User ID or Password"
            return render_template('login.html', error=error)
    return render_template('login.html')


@app.route('/home')
def home():
    if 'user' in session:
        user_name = db_ops.get_user_name(session['user']).title()
        return render_template('home.html', username=user_name)
    else:
        return redirect(url_for('login'))
@app.route('/reports')
def report():
    if 'user' in session:
        user_name = db_ops.get_user_name(session['user']).title()
        return render_template('reports.html', username=user_name)
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


@app.route('/get_last_sample_id')
def get_last_sample_id_route():
    last_sample_id = db_ops.get_last_sample_id()
    return jsonify(last_sample_id)


@app.route('/get_analysis_id')
def get_analysis_id_r():
    analysis_id = db_ops.get_analysis_id()
    return jsonify(analysis_id)


@app.route('/sample_form')
def sample_form():
    if 'user' not in session:
        return redirect(url_for('login'))

    last_sample_id = db_ops.get_last_sample_id()
    next_sample_id = (last_sample_id + 1) if last_sample_id else 1
    user_name = db_ops.get_user_name(session['user']).title()
    return render_template('sample_form.html', userid=session['user'], sampleID=next_sample_id, username=user_name)


@app.route('/analyse_form')
def analyse_form():
    if 'user' not in session:
        return redirect(url_for('login'))
    last_analysis_id = db_ops.get_analysis_id()
    next_analysis_id = (last_analysis_id + 1) if last_analysis_id else 1
    user_name = db_ops.get_user_name(session['user']).title()
    return render_template('analyse_form.html', userid=session['user'], analysisID=next_analysis_id, username=user_name)


@app.route('/get_materials')
def get_materials_route():
    materials = db_ops.get_materials()
    return jsonify(materials)


@app.route('/get_sample_points')
def get_sample_points_route():
    material = request.args.get('material')
    sample_points = db_ops.get_sample_points(material)
    return jsonify(sample_points)


@app.route('/get_values')
def get_val_route():
    sampleID = request.args.get('sampleID')
    values = db_ops.get_values(sampleID)
    return jsonify(values)


@app.route('/get_lab')
def get_lab_route():
    labID = request.args.get('lab')
    labname = db_ops.get_lab(labID)
    return jsonify(labname)


@app.route('/get_sam')
def get_sam_route():
    samplerID = request.args.get('samplerID')
    samplername = db_ops.get_sampler(samplerID)
    return jsonify(samplername)


@app.route('/get_limits')
def get_limits_route():
    material = request.args.get('material')
    limits = db_ops.get_limits(material)
    if limits:
        return jsonify(limits)
    else:
        return jsonify({'error': 'No limits found for the specified material'})


@app.route('/get_lab_name')
def get_lab_name_route():
    lab_name = db_ops.get_lab_name()
    return jsonify(lab_name)


@app.route('/get_sampler')
def get_sampler_route():
    sampler_ids = db_ops.get_sampler_id()
    return jsonify(sampler_ids)


@app.route('/get_sample_id')
def get_sampleid():
    sample_id = db_ops.get_sample_id()
    return jsonify(sample_id)


@app.route('/unanalys_sample_id')
def un_sampleid():
    sample_n = db_ops.unanalys_sample_id()
    return jsonify(sample_n)


@app.route('/last_sample_id')
def la_sampleid():
    sample_ns = db_ops.last_sample_id_ana()
    return jsonify(sample_ns)


@app.route('/get_test_req')
def get_test_req_route():
    material = request.args.get('material')
    test_req = db_ops.get_test_req(material)
    return jsonify(test_req)
@app.route('/get_std_test')
def get_std_test_route():
    material = request.args.get('material')
    sampleType = request.args.get('sampleType')
    test = db_ops.get_std_test(material,sampleType)
    return jsonify(test)

@app.route('/fetch_data')
def fetch_data():
    data = db_ops.get_data()
    if data:
        formatted_data = [
            {
                "AnalysisID": row[0],
                "SampleID": row[1],
                "Lab": row[2],
                "TestType": row[3],
                "UserID": row[4],
                "Material": row[5],
                "MC": row[6],
                "OC": row[7],
                "FFA": row[8],
                "FM": row[9],
                "SS": row[10],
                "Protein": row[11],
                "CLR": row[12],
                "MIV": row[13],
                "EO": row[14],
                "IV": row[15],
                "SV": row[16],
                "DateTime": row[17].strftime("%Y-%m-%d %H:%M:%S"),
                "Remarks": row[18]
            }
            for row in data
        ]
         
        return jsonify(formatted_data)
    else:
        return jsonify({"error": "No data found for Sample ID"}), 404

@app.route('/submit_sample', methods=['POST'])
def submit_form():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        parameters = {
            'sampleID': request.form['sampleID'],
            'lab': request.form['lab'],
            'samplerID': request.form['samplerID'],
            'datetime': request.form['datetime'],
            'userID':  session['user'],
            'sampleType': request.form['sampleType'],
            'material': request.form['material'],
            'partyName': request.form.get('partyName', ''),
            'batchID': request.form.get('batchID', ''),
            'samplePoint': request.form['samplePoint'],
            'qtyMt': request.form['qtyMt'],
            'testReqCheckbox': request.form['tst'],
            'parameter_1': request.form.get('parameter_1', ''),
            'parameter_2': request.form.get('parameter_2', ''),
            'parameter_3': request.form.get('parameter_3', ''),
            'parameter_4': request.form.get('parameter_4', ''),
            'parameter_5': request.form.get('parameter_5', ''),
            'parameter_6': request.form.get('parameter_6', ''),
            'datetime_stmp': datetime.now()
        }

        sql = """INSERT INTO samplereg (SampleID, SamplerID, Date_time, LabID, UserID, Material, 
                SampleType, PartyName, BatchID_VhNo, SmplPt, QtyMt, Test_RQMT,
                Parameter_1, Parameter_2, Parameter_3, Parameter_4,
                Parameter_5, Parameter_6, Date_time_stmp)
                VALUES (%(sampleID)s, %(samplerID)s, %(datetime)s, %(lab)s, %(userID)s, %(material)s,
            %(sampleType)s, %(partyName)s, %(batchID)s, %(samplePoint)s, %(qtyMt)s, %(testReqCheckbox)s,
            %(parameter_1)s, %(parameter_2)s, %(parameter_3)s, %(parameter_4)s,
            %(parameter_5)s, %(parameter_6)s, %(datetime_stmp)s)"""

        cursor.execute(sql, parameters)
        conn.commit()
        cursor.close()
        session['form_data'] = request.form
        session['submission_time'] = str(datetime.now())

        return "Success", 200
    except mysql.connector.Error as e:
        conn.rollback()
        error_message = str(e) + 500
        return render_template('error.html', error_message=error_message), 500
    finally:
        conn.close()


@app.route('/submit_analysis', methods=['POST'])
def submit_ana_form():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        parameters = {
            'SampleID': request.form['sampleID'],
            'LabID': request.form['lab'],
            'TestType': request.form['testType'],
            'UserID': session['user'],
            'Material': request.form['material'],
            'M_C': request.form['M_C'] or None,
            'O_C': request.form['O_C'] or None,
            'FFA': request.form['FFA'] or None,
            'FM': request.form['FM'] or None,
            'SS': request.form['SS'] or None,
            'PROTEIN': request.form['protein'] or None,
            'CLR': request.form['CLR'] or None,
            'MIV': request.form['MIV'] or None,
            'EO': request.form['EO'] or None,
            'IV': request.form['IV'] or None,
            'SV': request.form['SV'] or None,
            'Date_Time_Stmp': datetime.now(),
            'Remarks': request.form['remarks'] or None
        }

        sql = """
    INSERT INTO analysisreg (SampleID, LabID, TestType, UserID, Material, M_C, O_C, FFA, FM, SS, PROTEIN, CLR, MIV, EO, IV, SV, Date_Time_Stmp, Remarks)
    VALUES (%(SampleID)s, %(LabID)s, %(TestType)s, %(UserID)s, %(Material)s, %(M_C)s, %(O_C)s, %(FFA)s, %(FM)s, %(SS)s, %(PROTEIN)s, %(CLR)s, %(MIV)s, %(EO)s, %(IV)s, %(SV)s, %(Date_Time_Stmp)s, %(Remarks)s)
"""

        cursor.execute(sql, parameters)
        conn.commit()
        cursor.close()

        session['form_data'] = request.form.to_dict()
        session['submission_time'] = parameters['Date_Time_Stmp'].strftime(
            '%Y-%m-%d %H:%M:%S')

        return "Success", 200

    except Exception as e:
        conn.rollback()
        error_message = str(e)

        print("Error: ", error_message)

        return render_template('error.html', error_message=error_message), 500

    finally:
        conn.close()



@app.route('/success')
def success():

    form_data = session.get('form_data', {})
    submission_time = session.get('submission_time', None)
    return render_template('success.html', data=form_data, submission_time=submission_time)


@app.route('/success2')
def success2():
    form_data = session.get('form_data', {})
    submission_time = session.get('submission_time', None)
    return render_template('success2.html', data=form_data, submission_time=submission_time)


@app.route('/error')
def error():
    return render_template('error.html')


dash_app = DailyReportDashboard(app)
dash_app_monthly = DailyReportDashboardMonthly(app)
dispatch_dashboard = DispatchDashboard(app)
plot_app = CombinedDashboard(app)
dispatch_monthly = DispatchMonthly(app)
if __name__ == '__main__':
    app.run(debug=True)

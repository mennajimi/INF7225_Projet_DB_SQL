from flask import Flask, render_template, request, redirect, url_for, flash
import os
from os.path import join, dirname, realpath

import pandas as pd
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'

# enable debugging mode
app.config["DEBUG"] = True

# Upload folder
app.config['UPLOAD_FOLDER'] = 'static'
ALLOWED_EXTENSIONS = set(['csv'])

# Database connexion
conn = sqlite3.connect('/Users/myriamennajimi/test_database',check_same_thread=False)
cursor = conn.cursor()
conn.commit()

#global variables
upld=False
query=''


# Root URL
@app.route('/')
def index():
     # Set The upload HTML template '\templates\index1.html'
    return render_template('index1.html',upload=upld)


# Get the uploaded files
@app.route("/", methods=['POST'])
def uploadFiles():
    global upld
      # get the uploaded file
    uploaded_file = request.files['file']
    if uploaded_file.filename == '':
        flash('No selected file')
    if uploaded_file.filename != '' and allowed_file(uploaded_file.filename):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
              # set the file path
        uploaded_file.save(file_path)
        CSVtoDF(file_path)
              # save the file
        flash('Your file was uploaded')
        upld=True
    return render_template('index1.html', upload=upld)

#Get query menu to be able to choose your type of query
@app.route("/query", methods=['GET','POST'])
def queryMenu():
    if request.method == "GET":
        return render_template('query.html')
    else:
        querytype = request.form["querytype"]
        return render_template("query.html", query=querytype)

#from the query option
@app.route("/results", methods=["POST"])
def queryResults():
    querytype = request.form["querytype"]
    if querytype == "A":
        lims = request.form["lims"]
        panel = request.form["panel"]
        row_data = QueryA(lims, panel)
        return render_template('results.html', query=querytype, lims=lims, panel=panel, data=row_data)
    if querytype == "B":
        subjID = request.form["subjID"]
        study = request.form["study"]
        row_data = QueryB(subjID, study)
        return render_template('results.html', query=querytype, subjID=subjID, study=study, data=row_data)
    if querytype == "C":
        ExpName = request.form["ExpName"]
        row_data = QueryC(ExpName)
        return render_template('results.html', query=querytype, ExpName=ExpName, data=row_data)
    if querytype == "D":
        study = request.form["study"]
        row_data = QueryD(study)
        return render_template('results.html', query=querytype, study=study, data=row_data)

def CSVtoDF(filePath):
    # Use Pandas to parse the CSV file
    CSVdata = pd.read_csv(filePath)
    df = pd.DataFrame(CSVdata)
    # Loop through the Rows and insert csv in DB
    for row in df.itertuples():
        if row.Qced == 'Y':
            insertPatient = (row.LIMSuniqueID, row.StudyCode, row.SubjectID, row.VisitID, row.TimePoint, row.SpecimenType, row.RunNumber)
            sqlPatient = '''INSERT OR REPLACE INTO Patient
                (LIMSuniqueID,StudyCode,SubjectID,VisitID,TimePoint,SpecimenType,RunNumber)
                VALUES (?,?,?,?,?,?,?)
                '''
            insertCondition = (row.RunNumber, row.TemperatureReport, row.Comments, row.StabilityStatus, row.ReceptionDateandTime,
                  row.ProcessingDateandTime, row.LIMSuniqueID, row.PANEL)
            sqlCondition = '''INSERT OR REPLACE INTO ConditionExp
                (RunNumber,TemperatureReport,Commentaire,Stability,DateReception,DateProcessing,LIMSuniqueID,Panel)
                VALUES (?,?,?,?,?,?,?,?)
                '''
            insertExp = (row.RunNumber, row.ExperimentName)
            sqlExp = '''INSERT OR REPLACE INTO EXPERIMENT
                (RunNumber,ExperimentName)
                VALUES (?,?)
                '''
            cursor.execute(sqlPatient, insertPatient)
            cursor.execute(sqlCondition, insertCondition)
            cursor.execute(sqlExp, insertExp)
    conn.commit()

#verify that it's the right extansion
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#Query function

#ValueA of query.html
#B)Select all conditions for a given sample
def QueryA(limsID,panel):
    sqlB= '''SELECT * FROM ConditionExp
            WHERE LIMSuniqueID = (?) and PANEL= (?)'''
    insertB= (limsID,panel)
    cursor.execute(sqlB, insertB)
    rows = cursor.fetchall()
    return rows

#Value B of query.html
#A)Select all the experiments for a given Patient
def QueryB(subjID,studyA):
    sqlA= '''SELECT exp.ExperimentName
            FROM EXPERIMENT Exp
            JOIN Patient pat ON exp.RunNumber=pat.RunNumber
            WHERE pat.SubjectID = (?) and pat.StudyCode= (?)'''
    insertA= (subjID,studyA)
    cursor.execute(sqlA, insertA)
    rows = cursor.fetchall()
    return rows


#ValueC of query.html
#C)Select patient information for a specific experiment
def QueryC(expName):
    sqlC = '''SELECT pat.LIMSuniqueID, pat.SubjectID, pat.VisitID, pat.TimePoint
                FROM Patient pat
                JOIN EXPERIMENT exp ON exp.RunNumber=pat.RunNumber
                WHERE exp.ExperimentName = (?)'''
    cursor.execute(sqlC, (expName,))
    rows = cursor.fetchall()
    return rows

#ValueD of query.html
#D)Select patient information for a specific study
def QueryD(studyD):
    sqlD = '''SELECT pat.LIMSuniqueID, pat.SubjectID,pat.VisitID,pat.TimePoint,exp.ExperimentName FROM Patient pat
            JOIN Experiment exp ON exp.RunNumber=pat.RunNumber
            WHERE StudyCode = (?)
            ORDER BY ExperimentName'''
    cursor.execute(sqlD, (studyD,))
    rows = cursor.fetchall()
    return rows




if (__name__ == "__main__"):
    app.run(port = 4999)

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import sqlite3
from collections import Counter
from pathlib import Path

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

def home(request):
    return render(request,'index.html')


# Create your views here.
@csrf_exempt

def addBug(request):
    return render(request,'addBug.html')


@csrf_exempt
def update_record(request,ReporterID):

    if request.method == 'POST':
        reporterName1 = request.POST.get('reporterName1')
        bugType1 = request.POST.get('bugType1')
        reason1 = request.POST.get('bugReason1')
        siteName1 = request.POST.get('siteName1')
        siteLink1 = request.POST.get('siteLink1')
        ownerEmail1 = request.POST.get('ownerEmail1')
        
        with sqlite3.connect(BASE_DIR/'data.db') as db:
            cursor=db.cursor()
            # Update the patient information in the database
            query = """
                UPDATE Form
                SET ReporterName = ?,
                    BugType = ?,
                    Reason = ?,
                    SiteName = ?,
                    SiteLink = ?,
                    OwnerEmail = ?
                WHERE ReporterID = ? 
            """
            values = (reporterName1, bugType1, reason1, siteName1, siteLink1, ownerEmail1, ReporterID )
            cursor.execute(query, values)
        
    return redirect('/record')
    
    
def delete_record(request,ReporterID):

    with sqlite3.connect(BASE_DIR / 'data.db') as db:
        cursor = db.cursor()
        query = "DELETE FROM Form WHERE ReporterID = ?"
        cursor.execute(query, (ReporterID,))
             
    return redirect('/record')
def fetch_records_and_count_reporters(request):
    with sqlite3.connect(BASE_DIR / 'data.db') as db:
        cursor = db.cursor()
        query = "SELECT ReporterName, COUNT(*) AS Records FROM Form GROUP BY ReporterName"
        cursor.execute(query)
        rows = cursor.fetchall()

        # Prepare the data as a list of dictionaries
        reporter_records = {}
        for row in rows:
            reporter_name = row[0]
            records = row[1]
            if reporter_name not in reporter_records:
                reporter_records[reporter_name] = records
            else:
                reporter_records[reporter_name] += records
        # print(reporter_records)
        
        # Calculate the total number of records
        total_records = sum(reporter_records.values())

        # Calculate the progress for each reporter
        record = []
        for reporter_name, records in reporter_records.items():
            progress = (records / total_records) * 100
            record.append({'name': reporter_name, 'progress': progress})

    return render(request, 'record.html', {'record': record})

def record(request):
    
    with sqlite3.connect(BASE_DIR / 'data.db') as db:
        cursor = db.cursor()
        query = "SELECT ReporterID, ReporterName, BugType, Reason, SiteName, SiteLink, OwnerEmail FROM Form"
        cursor.execute(query)
        row = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]

            # Prepare the data as a list of dictionaries
        record = []
        for row in row:
            r = dict(zip(column_names, row))
            record.append(r)
    
    return render(request,'record.html',{'record':record})



@csrf_exempt
def saveform(request):
    if request.method == 'POST':
        reporterName = request.POST.get('reporterName')
        bugType = request.POST.get('bugType')
        reason = request.POST.get('bugReason')
        siteName = request.POST.get('siteName')
        siteLink = request.POST.get('siteLink')
        ownerEmail = request.POST.get('ownerEmail')

        with sqlite3.connect(BASE_DIR / 'data.db') as db:
            cursor = db.cursor()

            # Get the last inserted reporter ID from the database
            query_last_id = "SELECT ReporterID FROM Form ORDER BY ReporterID DESC LIMIT 1"
            cursor.execute(query_last_id)
            result = cursor.fetchone()

            if result is not None:
                last_id = int(result[0])
                new_id = str(last_id + 1).zfill(4)  # Increment the last ID and pad with leading zeros
            else:
                new_id = "0001"  # If there are no existing records, start with 0001

            query = "INSERT INTO Form (ReporterID, ReporterName, BugType, Reason, SiteName, SiteLink, OwnerEmail) VALUES (?, ?, ?, ?, ?, ?, ?)"
            values = (new_id, reporterName, bugType, reason, siteName, siteLink, ownerEmail)
            cursor.execute(query, values)

    return render(request, 'addBug.html')



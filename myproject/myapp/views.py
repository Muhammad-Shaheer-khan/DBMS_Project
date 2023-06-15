from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

import sqlite3
import random
import string


from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

def home(request):
    return render(request,'index.html')


# Create your views here.
@csrf_exempt

def addBug(request):
    return render(request,'addBug.html')


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
        
        # print(status)

        

    
    return render(request,'record.html',{'record':record})

@csrf_exempt
def saveform(request):
    if request.method=='POST':
        # bugID=request.POST.get('bugNumber')
        reporterName=request.POST.get('reporterName')
        bugType=request.POST.get('bugType')
        reason=request.POST.get('bugReason')
        siteName=request.POST.get('siteName')
        siteLink=request.POST.get('siteLink')
        ownerEmail=request.POST.get('ownerEmail')
        with sqlite3.connect(BASE_DIR/'data.db') as db:
            cursor=db.cursor()
            query = "INSERT INTO Form (ReporterID,ReporterName,BugType,Reason,SiteName,SiteLink,OwnerEmail) VALUES (?, ?,?,?,?,?,?)"
            values = ("".join(random.choices(string.digits, k=4)),reporterName,bugType,reason,siteName,siteLink,ownerEmail)
            cursor.execute(query, values)
            
        
    return render(request,'addBug.html')
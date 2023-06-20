from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import sqlite3
from django.http import JsonResponse
from pathlib import Path
from django.http import HttpResponseBadRequest, HttpResponse
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

def home(request):
    return render(request,'index.html')


# Create your views here.
@csrf_exempt

def addBug(request):
    return render(request,'addBug.html')


def email(request):
    return render(request,'email.html')

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

def record(request):
    
    with sqlite3.connect(BASE_DIR / 'data.db') as db:
        cursor = db.cursor()
        
        cursor1=db.cursor()
        cursor2=db.cursor()

        query = "SELECT ReporterID, ReporterName, BugType, Reason, SiteName, SiteLink, OwnerEmail FROM Form"
        cursor.execute(query)
        row = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]

            # Prepare the data as a list of dictionaries
        record = []
        for row in row:
            r = dict(zip(column_names, row))
            record.append(r)
            
            
        query1 = "SELECT DISTINCT ReporterName FROM Form"
        cursor1.execute(query1)
        row1 = cursor1.fetchall()
        column_names1 = [description[0] for description in cursor.description]

            # Prepare the data as a list of dictionaries
        record1 = []
        for row in row1:
            r = dict(zip(column_names1, row))
            record1.append(r)
            
            
        query2 = "SELECT ReporterName, COUNT(*) AS Records FROM Form GROUP BY ReporterName"
        cursor2.execute(query2)
        
        row2 = cursor2.fetchall()
        print(row2)
        column_names2 = [description[0] for description in cursor2.description]

        record2 = []
        for row in row2:
            r = dict(zip(column_names2, row))
            record2.append(r)
    return render(request,'record.html',{'record':record,'record1':record1,'record2':record2})


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




def email(request):
    reporters = Reporter.objects.all()
    return render(request, 'email.html', {'reporters': reporters})

def fetch_bug_types(request):
    reporter_id = request.GET.get('reporter')
    bug_types = BugType.objects.filter(reporter_id=reporter_id).values_list('name', flat=True)
    return JsonResponse({'bug_types': list(bug_types)})

def fetch_site_names(request):
    reporter_id = request.GET.get('reporter')
    bug_type = request.GET.get('bug_type')
    site_names = SiteName.objects.filter(reporter_id=reporter_id, bug_type=bug_type).values_list('name', flat=True)
    return JsonResponse({'site_names': list(site_names)})

def fetch_owner_names(request):
    reporter_id = request.GET.get('reporter')
    bug_type = request.GET.get('bug_type')
    site_name = request.GET.get('site_name')
    owner_names = OwnerName.objects.filter(reporter_id=reporter_id, bug_type=bug_type, site_name=site_name).values_list('name', flat=True)
    owner_email = OwnerName.objects.filter(reporter_id=reporter_id, bug_type=bug_type, site_name=site_name).values_list('email', flat=True).first()
    return JsonResponse({'owner_names': list(owner_names), 'owner_email': owner_email})
from django.shortcuts import render

def home(request):
    return render(request,'index.html')

# Create your views here.
def addBug(request):
    return render(request,'addBug.html')


def record(request):
    return render(request,'record.html')
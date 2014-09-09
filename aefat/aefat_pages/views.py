from django.shortcuts import render

# Create your views here.
def aefat(request):
    return render(request, 'aefat_pages/home.html')

def home(request):
    return render(request, 'aefat_pages/home.html')
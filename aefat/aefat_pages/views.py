from django.shortcuts import render

# Create your views here.
def aefat(request):
    return render(request, 'aefat_pages/index.html')

def aefat_home(request):
    return render(request, 'aefat_pages/index.html')
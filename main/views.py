from django.shortcuts import render

def index(request):
    return render(request, "main/index.html")
# Create your views here.
def news(request):
    return render(request, "main/news.html")

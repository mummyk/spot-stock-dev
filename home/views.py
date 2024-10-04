from django.shortcuts import render

# Create your views here.


def home(request):
    context = {'title': "Welcome Home"}
    return render(request, 'index.html', context)

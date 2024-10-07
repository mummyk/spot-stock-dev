from django.shortcuts import render

# Create your views here.


def company(request):
    context = {'title': "Your Company", }
    return render(request, 'company/get_all.html', context)

from django.shortcuts import render

# Create your views here.


def getCompanyList(request):
    context = {'title': 'Your companies', 'companies': []}

    return render(request, 'company/list_company.html', context)

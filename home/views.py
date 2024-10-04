from django.shortcuts import render, redirect

# Create your views here.


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    context = {'title': "Welcome Home"}
    return render(request, 'index.html', context)


def handler404(request, exception):
    return render(request, 'errors/404.html', status=404)


def handler500(request):
    return render(request, 'errors/500.html', status=500)


def handler403(request, exception):
    return render(request, 'errors/403.html', status=403)


def handler400(request, exception):
    return render(request, 'errors/400.html', status=400)

from django.shortcuts import render


def index(request):
    return render(request, template_name="www/index.html", context={})


def error(request):
    raise Exception()

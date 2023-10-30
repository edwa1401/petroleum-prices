from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from users.models import User


def index(request: HttpRequest) -> HttpResponse:
    users = User.objects.all()

    context = {
        'users': users,
    }
    return render(request, 'index.html', context=context)

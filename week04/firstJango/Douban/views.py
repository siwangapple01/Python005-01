from django.shortcuts import render
from django.views.generic import ListView

from django.http import HttpResponse
from .models import DoubanComment


def index(request):
    # return render(request, 'index.html', locals())

    all_records = DoubanComment.objects.all()
    condtions = {'n_star__gt': 3}
    shorts = all_records.filter(**condtions)
    return render(request, 'index.html', locals())

# Create your views here.


def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)


def search(request):

    all_records = DoubanComment.objects.all()
    q = request.GET.get('q')

    conditions = {'short__icontains': q}
    search = all_records.filter(**conditions).all()

    return render(request, 'search.html', locals())

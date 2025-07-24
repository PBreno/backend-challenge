import os.path

from django.core.paginator import Paginator
from django.shortcuts import render
from .models import *
# Create your views here.

def index(request):

    #create_file(data)
    players_registered = read_file()
    #paginator = Paginator(players_registered, 10)
    #page_number = request.GET.get('page')
    #page = paginator.get_page(page_number)


    context = {
        'page': players_registered,
        'site_title': 'Player Registration System',
    }

    return render(request, 'prs/index.html', context)
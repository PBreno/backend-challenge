import json
from pathlib import Path

from django.db import models
from django.shortcuts import redirect, render

from .forms import RegisterForm

# Create your models here.
BASE_DIR = Path(__file__).resolve().parent.parent
def create_file(data):

    path = BASE_DIR /'data.json'
    if not data:
        return {
            'message': 'File not found.',
        'data': None}

    try:
        with open(path, "w") as file:
            json.dump(data, file, indent=4)

    except FileNotFoundError as e:
        print(e)
        return None

def read_file():

    try:

        with open(BASE_DIR / 'data.json', 'r') as file:
            json_data = json.load(file)
            return json_data
    except FileNotFoundError as e:
        return e

def register(request):

    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('prs:index')

    return render(
        request,
        'prs/register.html',
        {'form': form,}
    )
class Files:

    def read(self):
        return 0
import json
import xml.etree.ElementTree as ET
from pathlib import Path

from django.db import models
from django.shortcuts import redirect, render
from django.urls import reverse

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
        data=request.POST
        form = RegisterForm(data)

        print("===")
        print('escolhido: ', data['group'])
        group_chosen(int(data['group']))
       # print(data['group'])
        print("===")


        if form.is_valid():
            form.save()
            return redirect('prs:index')


    return render(
        request,
        'prs/register.html',
        {'form': form,}
    )

def group_chosen(group: int):
    codenome = []
    if group == 1:
        tree = ET.parse(BASE_DIR / 'referencias/liga_da_justica.xml')
        root = tree.getroot()

        for codinome in root.findall('codinomes'):
            for cod in codinome.findall('codinome'):
                codenome.append(cod.text)

        return codenome
    else:
       pass
class Files:

    def read(self):
        return 0
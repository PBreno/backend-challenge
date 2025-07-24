import json
import random
import urllib.request
import xml.etree.ElementTree as ET
from json import JSONDecodeError
from pathlib import Path
from django.contrib.auth.models import User
import requests
from django.shortcuts import redirect, render

from .forms import RegisterForm

# Create your models here.
BASE_DIR = Path(__file__).resolve().parent.parent

def read_file():

    try:
        for user in User.objects.all():
            print('User ->', user.username,'\t email-> ', user.email)

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
        player = dict(form.data)

        player.pop('csrfmiddlewaretoken')

        name = str(player['name']).replace("['", '').replace("']", '')
        email = str(player['email']).replace("['", '').replace("']", '')
        phone = str(player['phone']).replace("['", '').replace("']", '')
        codename = group_chosen(player.get('group'))
        group  = str(player.get('group')).replace("['", '').replace("']", '')

        player['name'] = name
        player['email'] = email
        player['phone'] = phone
        player['codename'] = codename
        player['group'] = group


        if form.is_valid():

            save_player(player)
            User.objects.all().delete()
            form.save()
            return redirect('prs:index')

    return render(
        request,
        'prs/register.html',
        {'form': form,}
    )


def group_chosen(group):

    codename = []
    string = str(group).replace("['", '').replace("']", '')

    if string == 'Liga da Justiça':
        url  = 'https://raw.githubusercontent.com/uolhost/test-backEnd-Java/master/referencias/liga_da_justica.xml'

        with urllib.request.urlopen(url) as response:
            xml_data = response.read()

        root = ET.fromstring(xml_data)

        for element in root.iter():
            codename.append(element.text)

        cod = random.choice(codename)

        return cod

    elif string == 'Os vingadores':

        url = 'https://raw.githubusercontent.com/uolhost/test-backEnd-Java/master/referencias/vingadores.json'
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception(response.status_code, response.text)

        data = response.json()
        cod = random.choice(data['vingadores']).get('codinome')

        return cod


def save_player(player):

    data = list()
    file_path = 'src/data.json'

    if not Path(file_path).exists() or not Path(file_path).stat().st_size:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except JSONDecodeError as e:
        return e

    try:
        data.append(player)
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except JSONDecodeError as e:
        return e
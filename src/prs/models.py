import json
import random
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

import requests
from django.shortcuts import redirect, render

from .forms import RegisterForm

# Create your models here.
BASE_DIR = Path(__file__).resolve().parent.parent

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
        player['codinome'] = codename
        player['group'] = group
        save_player(player)
        if form.is_valid():
            form.save()

            return redirect('prs:index')

    return render(
        request,
        'prs/register.html',
        {'form': form,}
    )


def group_chosen(group):

    codenome = []
    url = ''
    string = str(group).replace("['", '').replace("']", '')

    if string == 'Liga da Justiça':
        url  = 'https://raw.githubusercontent.com/uolhost/test-backEnd-Java/master/referencias/liga_da_justica.xml'

        with urllib.request.urlopen(url) as response:
            xml_data = response.read()

        root = ET.fromstring(xml_data)

        for element in root.iter():
            codenome.append(element.text)

        cod = random.choice(codenome)
        return cod

    elif string == 'Os vingadores':

        url = 'https://raw.githubusercontent.com/uolhost/test-backEnd-Java/master/referencias/vingadores.json'
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception(response.status_code, response.text)

        data = response.json()

        return random.choice(data['vingadores']).get('codinome')

    # {
    #     'vingadores':
    #         [
    #             {'codinome': 'Hulk'},
    #             {'codinome': 'Capitão América'},
    #             {'codinome': 'Pantera Negra'},
    #             {'codinome': 'Homem de Ferro'},
    #             {'codinome': 'Thor'},
    #             {'codinome': 'Feiticeira Escarlate'},
    #             {'codinome': 'Visão'}
    #         ]
    # }


def save_player(player):

    try:
        if not player:
            return

        with open ('src/data.json', 'a') as file:

            file.write("[")
            file.write(json.dumps(player, indent=4))
            file.write("]")


    except Exception as e:
        raise e


#class Files:

 #   def read(self):
  #      return 0
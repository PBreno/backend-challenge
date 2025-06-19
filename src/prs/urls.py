from django.urls import path
from . import views
app_name = 'prs'

urlpatterns = [

    path('', views.index, name='index'),
]
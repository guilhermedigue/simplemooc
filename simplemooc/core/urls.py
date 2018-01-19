from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
    path('', views.home, name='home'),
    path('contato/', views.contact, name='contact'),
    #url(r'^contato/$', views.contact, name='contact'),
]

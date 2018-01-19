from django.conf.urls import url
from django.contrib.auth import views
from django.urls import path, include
from . import views as v_ac

app_name = 'accounts'
urlpatterns = [
    path('', v_ac.dashboard, name='dashboard'),
    path('entrar/', views.login, {'template_name': 'accounts/login.html'}, name='login'),
    path('sair/', views.logout, {'next_page': 'core:home'}, name='logout'),
    path('cadastrar/', v_ac.register, name='register'),
    path('nove-senha/', v_ac.password_reset, name='password_reset'),
    url(r'^confirmar-nova-senha/(?P<key>\w+)/$', v_ac.password_reset_confirm, name='password_reset_confirm'),
    path('edit/', v_ac.edit, name='edit'),
    path('edit-senha/', v_ac.edit_password, name='edit_password'),
]

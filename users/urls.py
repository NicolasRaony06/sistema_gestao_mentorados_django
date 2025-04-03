from django.urls import path
from . import views
from django.http import HttpResponse

urlpatterns = [
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login, name='login'),
]

from django.urls import path
from . import views
from django.http import HttpResponse

urlpatterns = [
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', lambda requets: HttpResponse('Em breve!'), name='login'),
]

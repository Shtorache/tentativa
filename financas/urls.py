from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('adicionar/', views.adicionar, name='adicionar'),
    path('exportar/', views.exportar_csv, name='exportar'),

    # NOVO
    path('acesso/<str:pessoa>/', views.escolher_pessoa, name='escolher_pessoa'),
    path('sair/', views.sair, name='sair'),
    path('lista/', views.lista_detalhada, name='lista_detalhada'),


]

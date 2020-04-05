from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:address_id>/', views.show_map, name = 'map'),
]
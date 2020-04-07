from django.urls import path
from . import views

urlpatterns = [
    path('', views.land, name='wegmans-land'),
    path('pre-generated/', views.pregenerated, name='wegmans-pre'),
    path('generated/', views.generated, name='wegmans-generated'),
]

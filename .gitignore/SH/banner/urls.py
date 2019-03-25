from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search', views.banner_list, name='banner_list'),
    path('load', views.model_form_upload, name='model_form_upload'),
    path('upload', views.simple_upload, name='simple_upload'), 
    path('view', views.view_list, name='view_list'), 
    path('test', views.test, name='test'),
    path('graph', views.graph, name='graph'),    
]
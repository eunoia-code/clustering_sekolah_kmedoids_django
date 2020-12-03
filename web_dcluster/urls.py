from django.conf.urls import url, include
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.conf import settings
from .views import data_list

from django.urls import path
from rest_framework import routers, serializers, viewsets
from . import views

router = routers.DefaultRouter()
router.register('siswa', views.SiswaViewSet, basename='siswa')
router.register('cluster_siswa', views.ClusterViewSet, basename='cluster_siswa')
router.register('sekolah', views.SekolahViewSet, basename='sekolah')
router.register('cluster', views.AllClusterViewSet, basename='cluster')
router.register('grup_cluster', views.GroupClusterViewSet, basename='grup_cluster')

urlpatterns = [
    url(r'^home/$', views.index, name='index'),
    url(r'^cluster/$', views.cluster_list, name='cluster'),
    url(r'^$', LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^data/$', data_list, name='data'),
    url(r'^update/(?P<id>\d+)/', views.update, name='update'),
    url(r'^delete/(?P<id>\d+)/', views.delete, name='delete'),
    url(r'^create_data/$', views.create_data, name='create_data'),
    url(r'^home2/$', views.index2, name='index2'),
    url(r'^upload-csv/$', views.csv, name="csv"),
    path('getDataCluster/', include(router.urls))
    
]

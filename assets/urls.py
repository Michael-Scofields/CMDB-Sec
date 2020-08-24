from django.urls import path
from assets import views


app_name = 'assets'


urlpatterns = [
    path('index/', views.index, name='index'),
    path('index/server/', views.index, name='index/server'),
    path('index/security/', views.index, name='index/security'),
    path('index/network/', views.index, name='index/network'),
    path('index/other/', views.index, name='index/other'),
    path('report/', views.report, name='report'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('detail/<int:asset_id>/', views.detail, name='detail'),
    path('', views.dashboard),
]

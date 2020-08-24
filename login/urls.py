from django.urls import path
from login import views
from assets import views as views_assets


app_name = 'login'


urlpatterns = [
    path('index/', views_assets.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('', views.login, name='login'),
]

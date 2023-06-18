from django.urls import path
from . import views

urlpatterns = [
    path('Signup/', views.Signup, name='Signup'),
    path('Login/', views.Loginpage, name='Login'),
    path('logout/', views.logout_page, name='logout'),
    path('upload/', views.Upload, name='Upload'),
    path('', views.home, name='home'),
    path('public_musicplayer/<int:id>/', views.public_musicplayer , name='public_musicplayer'),
    path('musicplayer/<int:id>/', views.musicplayer , name='musicplayer'),
    path('account_home/', views.account_home , name='account_home'),
    path('account_upload/', views.account_upload , name='account_upload'),
    path('account_protect/', views.account_protect , name='account_protect'),
    path('account_private/', views.account_private , name='account_private'),
]

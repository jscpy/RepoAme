from django.urls import path
from django.contrib.auth import views as auth_views
from repo_ita import views

app_name = 'repo_ita'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('articulos/', views.articulo, name='articulos'),
    path('articulos/create', views.create_articulo, name='articulo-create'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout')
]

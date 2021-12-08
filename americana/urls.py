from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth import views as auth_views
from americana import views

app_name = 'repo-ame'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('tablero/', views.Tablero.as_view(), name='tablero'),
    path('tesis/', views.TesisListView.as_view(), name='tesis'),
    path('tesis/new/', views.TesisCreateView.as_view(), name='tesis-create'),
    path('tesis/list/', views.TesisUserListView.as_view(), name='tesis-list'),
    path('tesis/<int:pk>/update', views.TesisUpdateView.as_view(), name='tesis-update'),
    path('tesis/<int:pk>/delete', views.TesisDeleteView.as_view(), name='tesis-delete'),
    path('congreso/', views.CongresoListView.as_view(), name='congreso'),
    path('congreso/new/', views.CongresoCreateView.as_view(), name='congreso-create'),
    path('congreso/list/', views.CongresoUserListView.as_view(), name='congreso-list'),
    path('congreso/<int:pk>/update', views.CongresoUpdateView.as_view(), name='congreso-update'),
    path('congreso/<int:pk>/delete', views.CongresoDeleteView.as_view(), name='congreso-delete'),
    path('signup/', views.signup, name='signup'),
    path('profile/update/', views.update_profile, name='profile-update'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout')
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )

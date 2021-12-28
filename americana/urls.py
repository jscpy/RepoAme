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
    path('tesis/list/', views.TesisUserListView.as_view(), name='tesis-list'),
    path('publicaciones/', views.PublicacionListView.as_view(), name='publicacion'),
    path('publicaciones/list/', views.PublicacionUserListView.as_view(), name='publicacion-list'),
    path('signup/', views.signup, name='signup'),
    path('profile/update/', views.update_profile, name='profile-update'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout')
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )

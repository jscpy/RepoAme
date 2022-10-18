from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.urls import path

from americana import views

app_name = 'repo-ame'

urlpatterns = [
    path('', views.index, name='home'),
    path('search', views.search, name='search'),
    path('tablero/', views.Tablero.as_view(), name='tablero'),

    # Tesis
    path('tesis/', views.TesisListView.as_view(), name='tesis'),
    path('tesis/<int:pk>/update', views.TesisUpdateView.as_view(), name='tesis-update'),
    path('tesis/<int:pk>/delete', views.TesisDeleteView.as_view(), name='tesis-delete'),
    path('tesis/modal/<int:pk>/', views.tesis_modal_summary, name='tesis-modal-summary'),

    # Publicaciones
    path('publicaciones/', views.PublicacionListView.as_view(), name='publicacion'),
    path('publicacion/<int:pk>/update', views.PublicacionUpdateView.as_view(), name='publicacion-update'),
    path('publicacion/<int:pk>/delete', views.PublicacionDeleteView.as_view(), name='publicacion-delete'),
    path('publicaciones/modal/<int:pk>/', views.publicacion_modal_summary, name='publicacion-modal-summary'),

    # path('signup/', views.signup, name='signup'),
    # path('profile/update/', views.update_profile, name='profile-update'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout')
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )

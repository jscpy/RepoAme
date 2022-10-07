from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth import views as auth_views
from americana import views

app_name = 'repo-ame'

new_urlpatters = [
    path('', views.new_index, name='home'),
    path('banner', views.banner, name='banner'),
    path('search/<int:pk>', views.filter_by_id, name='filter-by-id'),
    path('search/autor/<str:autor>', views.filter_by_autor, name='filter-by-autor'),
    path('search/area/<str:area>', views.filter_by_area, name='filter-by-area'),
    path('search/anio/<int:year>', views.filter_by_year, name='filter-by-year'),
]


urlpatterns = [
    # path('', views.Home.as_view(), name='home'),
    path('tablero/', views.Tablero.as_view(), name='tablero'),

    # Tesis
    path('tesis/', views.TesisListView.as_view(), name='tesis'),
    # path('tesis/list/', views.TesisUserListView.as_view(), name='tesis-list'),
    path('tesis/<int:pk>/update', views.TesisUpdateView.as_view(), name='tesis-update'),
    path('tesis/<int:pk>/delete', views.TesisDeleteView.as_view(), name='tesis-delete'),
    path('tesis/modal/<int:pk>/', views.tesis_modal_summary, name='tesis-modal-summary'),

    # Publicaciones
    path('publicaciones/', views.PublicacionListView.as_view(), name='publicacion'),
    # path('publicaciones/list/', views.PublicacionUserListView.as_view(), name='publicacion-list'),
    path('publicacion/<int:pk>/update', views.PublicacionUpdateView.as_view(), name='publicacion-update'),
    path('publicacion/<int:pk>/delete', views.PublicacionDeleteView.as_view(), name='publicacion-delete'),
    path('publicaciones/modal/<int:pk>/', views.publicacion_modal_summary, name='publicacion-modal-summary'),

    # path('signup/', views.signup, name='signup'),
    # path('profile/update/', views.update_profile, name='profile-update'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout')
] + new_urlpatters

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )

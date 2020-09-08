from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('players', views.players, name='players'),
    path('players/<int:player_id>/', views.player_details, name='player_details'),

    path('openings', views.openings, name='openings'),
    path('openings/<int:opening_id>/', views.opening_details, name='opening_details'),

    path('opening_systems', views.opening_systems, name='opening_systems'),
    path('opening_systems/<int:opening_system_id>/', views.opening_system_details, name='opening_system_details'),

    path('games', views.games, name='games'),
    path('games/<int:game_id>/', views.game_details, name='game_details'),
]

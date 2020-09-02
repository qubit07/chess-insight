from django.urls import path
from . import views

urlpatterns = [
    path('players', views.players, name='players'),
    path('players/<int:player_id>/', views.player_details, name='player_details'),
    path('openings', views.openings, name='openings'),
    path('games', views.games, name='games'),
    path('games/<int:game_id>/', views.game_details, name='game_details'),
]

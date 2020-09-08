from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import RequestContext, loader
from django.core.paginator import Paginator
from django.db.models import Count
from .models import User, Game, Opening, OpeningSystem


def dashboard(request):
    context = {
        'opening_systems': OpeningSystem.objects.all().order_by("name"),
    }
    return render(request, 'insight/dashboard.html', context)


def players(request):
    context = {
        'players': User.objects.all(),
    }
    return render(request, 'insight/players.html', context)

def player_details(request, player_id):
    player = get_object_or_404(User, id=player_id)
    context = {
        'player': player,
    }
    return render(request, 'insight/player_details.html', context)

def opening_systems(request):
    opening_systems = OpeningSystem.objects.filter(opening__game__elo_mean__lt=2200).annotate(count=Count('opening')).annotate(count=Count('opening__game')).order_by('-count')
    master_opening_systems =  OpeningSystem.objects.filter(opening__game__elo_mean__gt=2200).annotate(count=Count('opening')).annotate(count=Count('opening__game')).order_by('-count')

    paginator = Paginator(opening_systems, 10)
    opening_systems = paginator.get_page(1)

    paginator = Paginator(master_opening_systems, 10)
    master_opening_systems = paginator.get_page(1)

    context = {
        'opening_systems': opening_systems,
        'master_opening_systems': master_opening_systems,
    }
    return render(request, 'insight/opening_systems.html', context)

def opening_system_details(request, opening_system_id):
    opening_system = get_object_or_404(OpeningSystem, id=opening_system_id)
    openings = Opening.objects.filter(opening_system = opening_system_id).annotate(count=Count('game')).order_by('-count')
    context = {
        'opening_system': opening_system,
        'openings' : openings
    }
    return render(request, 'insight/opening_system_details.html', context)


def games(request):
    games = Game.objects.all().order_by('-timestamp')
    paginator = Paginator(games, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'insight/games.html', context)

def game_details(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    context = {
        'game': game,
    }
    return render(request, 'insight/game_details.html', context)

def openings(request):
    opening_list = Opening.objects.all()
    paginator = Paginator(opening_list, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'insight/openings.html', context)

def opening_details(request, opening_id):
    opening = get_object_or_404(Opening, id=opening_id)
    context = {
        'opening' : opening
    }
    return render(request, 'insight/opening_details.html', context)

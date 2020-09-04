from django.db import models

class User(models.Model):
    name = models.CharField(max_length=40)

class OpeningSystem(models.Model):
    name = models.CharField(max_length=40)

class Opening(models.Model):
    name = models.CharField(max_length=40)
    eco = models.CharField(max_length=3)
    opening_system = models.ForeignKey(OpeningSystem, on_delete=models.CASCADE)
    moves = models.TextField()

class Game(models.Model):
    elo_mean = models.IntegerField(default=0)
    elo_diff = models.IntegerField(default=0)
    result = models.CharField(max_length=40)
    opening = models.ForeignKey(Opening, on_delete=models.CASCADE)
    timecontrol = models.CharField(max_length=40)
    timestamp = models.DateTimeField()
    raw = models.TextField()

class Analyse(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    turnover_move = models.IntegerField(default=0)
    turnover_evaluation = models.IntegerField(default=0)
    unbalance_material = models.IntegerField(default=0)
    unbalance_officers = models.IntegerField(default=0)
    unbalance_exchange = models.IntegerField(default=0)

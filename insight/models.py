from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=40)
    elo = models.IntegerField(default=0);
    rank = models.IntegerField(default=0);
    skill = models.CharField(max_length=40, default='Peon')



class Game(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    raw = models.TextField()

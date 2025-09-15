from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import connection
from djongo import models


from octofit_tracker.models import Team, Activity, Leaderboard, Workout

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        User = get_user_model()
        # Delete all data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Create teams
        marvel = Team.objects.create(name='Team Marvel')
        dc = Team.objects.create(name='Team DC')

        # Create users (super heroes)
        users = [
            User(email='tony@marvel.com', username='IronMan', team=marvel),
            User(email='steve@marvel.com', username='CaptainAmerica', team=marvel),
            User(email='bruce@marvel.com', username='Hulk', team=marvel),
            User(email='clark@dc.com', username='Superman', team=dc),
            User(email='bruce@dc.com', username='Batman', team=dc),
            User(email='diana@dc.com', username='WonderWoman', team=dc),
        ]
        for user in users:
            user.set_password('password')
            user.save()

        # Create activities
        activities = [
            Activity(user=users[0], type='Run', duration=30, calories=300),
            Activity(user=users[1], type='Swim', duration=45, calories=400),
            Activity(user=users[2], type='Bike', duration=60, calories=500),
            Activity(user=users[3], type='Run', duration=25, calories=250),
            Activity(user=users[4], type='Swim', duration=35, calories=350),
            Activity(user=users[5], type='Bike', duration=50, calories=450),
        ]
        for activity in activities:
            activity.save()

        # Create workouts
        workouts = [
            Workout(name='Morning Cardio', description='Cardio for all heroes'),
            Workout(name='Strength Training', description='Strength for all heroes'),
        ]
        for workout in workouts:
            workout.save()

        # Create leaderboard
        Leaderboard.objects.create(team=marvel, points=1200)
        Leaderboard.objects.create(team=dc, points=1100)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))

# Models for reference (to be created in octofit_tracker/models.py):
# class Team(models.Model):
#     name = models.CharField(max_length=100)
#
# class Activity(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     type = models.CharField(max_length=50)
#     duration = models.IntegerField()
#     calories = models.IntegerField()
#
# class Workout(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#
# class Leaderboard(models.Model):
#     team = models.ForeignKey(Team, on_delete=models.CASCADE)
#     points = models.IntegerField()

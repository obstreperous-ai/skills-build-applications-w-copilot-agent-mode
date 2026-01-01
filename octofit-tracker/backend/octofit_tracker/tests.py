from django.test import TestCase
from .models import User, Team, Activity, Workout, Leaderboard

class ModelSmokeTest(TestCase):
    def test_team_create(self):
        team = Team.objects.create(name='Test Team', description='desc')
        self.assertIsNotNone(team.id)
    def test_user_create(self):
        team = Team.objects.create(name='T', description='d')
        user = User.objects.create(email='a@b.com', name='A', team=team, is_superhero=True)
        self.assertIsNotNone(user.id)
    def test_activity_create(self):
        team = Team.objects.create(name='T2', description='d2')
        user = User.objects.create(email='b@b.com', name='B', team=team, is_superhero=True)
        activity = Activity.objects.create(user=user, type='Run', duration=10, date='2024-01-01')
        self.assertIsNotNone(activity.id)
    def test_workout_create(self):
        workout = Workout.objects.create(name='W', description='desc')
        self.assertIsNotNone(workout.id)
    def test_leaderboard_create(self):
        team = Team.objects.create(name='T3', description='d3')
        leaderboard = Leaderboard.objects.create(team=team, points=100)
        self.assertIsNotNone(leaderboard.id)

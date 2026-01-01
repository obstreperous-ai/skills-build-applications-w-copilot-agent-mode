from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        # Clear existing data using Django ORM to maintain consistency
        Activity.objects.all().delete()
        Workout.objects.all().delete()
        Leaderboard.objects.all().delete()
        User.objects.all().delete()
        Team.objects.all().delete()

        # Now proceed with Django ORM population

        # Create Teams
        marvel = Team.objects.create(name='Marvel', description='Team Marvel Superheroes')
        dc = Team.objects.create(name='DC', description='Team DC Superheroes')

        # Create Users
        users = [
            User.objects.create(email='tony@marvel.com', name='Tony Stark', team=marvel, is_superhero=True),
            User.objects.create(email='steve@marvel.com', name='Steve Rogers', team=marvel, is_superhero=True),
            User.objects.create(email='bruce@marvel.com', name='Bruce Banner', team=marvel, is_superhero=True),
            User.objects.create(email='clark@dc.com', name='Clark Kent', team=dc, is_superhero=True),
            User.objects.create(email='diana@dc.com', name='Diana Prince', team=dc, is_superhero=True),
            User.objects.create(email='barry@dc.com', name='Barry Allen', team=dc, is_superhero=True),
        ]

        # Create Activities
        for user in users:
            Activity.objects.create(user=user, type='Running', duration=30, date=timezone.now().date())
            Activity.objects.create(user=user, type='Cycling', duration=45, date=timezone.now().date())

        # Create Workouts
        workout1 = Workout.objects.create(name='Super Strength', description='Strength training for superheroes')
        workout2 = Workout.objects.create(name='Speed Run', description='Speed training for speedsters')
        for user in users:
            workout1.suggested_for.add(user)
            workout2.suggested_for.add(user)

        # Create Leaderboards
        Leaderboard.objects.create(team=marvel, points=300)
        Leaderboard.objects.create(team=dc, points=250)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))

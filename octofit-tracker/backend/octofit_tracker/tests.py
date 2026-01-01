from django.test import TestCase
from django.core.exceptions import ValidationError
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

class UserEmailValidationTest(TestCase):
    def setUp(self):
        self.team = Team.objects.create(name='Test Team', description='Test team for validation')
    
    def test_valid_email(self):
        """Test that valid emails are accepted"""
        user = User.objects.create(email='valid@example.com', name='Valid User', team=self.team)
        self.assertIsNotNone(user.id)
        self.assertEqual(user.email, 'valid@example.com')
    
    def test_email_normalized_to_lowercase(self):
        """Test that emails are normalized to lowercase"""
        user = User.objects.create(email='Test@Example.COM', name='Test User', team=self.team)
        self.assertEqual(user.email, 'test@example.com')
    
    def test_blocked_disposable_email_domain(self):
        """Test that disposable email domains are blocked"""
        with self.assertRaises(ValidationError):
            User.objects.create(email='test@tempmail.com', name='Test User', team=self.team)
    
    def test_blocked_mailinator_domain(self):
        """Test that mailinator domain is blocked"""
        with self.assertRaises(ValidationError):
            User.objects.create(email='test@mailinator.com', name='Test User', team=self.team)
    
    def test_email_without_tld(self):
        """Test that emails without TLD are rejected"""
        with self.assertRaises(ValidationError):
            User.objects.create(email='test@localhost', name='Test User', team=self.team)
    
    def test_email_with_consecutive_dots_in_domain(self):
        """Test that domains with consecutive dots are rejected"""
        with self.assertRaises(ValidationError):
            User.objects.create(email='test@example..com', name='Test User', team=self.team)
    
    def test_email_with_consecutive_special_chars_in_local(self):
        """Test that local parts with consecutive special characters are rejected"""
        with self.assertRaises(ValidationError):
            User.objects.create(email='test..user@example.com', name='Test User', team=self.team)
    
    def test_email_too_long(self):
        """Test that excessively long emails are rejected"""
        long_email = 'a' * 250 + '@example.com'
        with self.assertRaises(ValidationError):
            User.objects.create(email=long_email, name='Test User', team=self.team)
    
    def test_email_local_part_too_long(self):
        """Test that local parts exceeding 64 characters are rejected"""
        long_local = 'a' * 65 + '@example.com'
        with self.assertRaises(ValidationError):
            User.objects.create(email=long_local, name='Test User', team=self.team)
    
    def test_email_with_whitespace_trimmed(self):
        """Test that whitespace is trimmed from email"""
        user = User.objects.create(email='  test@example.com  ', name='Test User', team=self.team)
        self.assertEqual(user.email, 'test@example.com')
    
    def test_valid_email_with_subdomain(self):
        """Test that valid emails with subdomains are accepted"""
        user = User.objects.create(email='user@mail.example.com', name='Test User', team=self.team)
        self.assertIsNotNone(user.id)
    
    def test_valid_email_with_plus_sign(self):
        """Test that valid emails with plus signs in local part are accepted"""
        user = User.objects.create(email='user+tag@example.com', name='Test User', team=self.team)
        self.assertIsNotNone(user.id)

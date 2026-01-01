from djongo import models
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
import re

def validate_email_domain(value):
    """
    Custom validator to ensure email domain is valid and not from suspicious patterns.
    Blocks common temporary email domains and validates domain structure.
    """
    # List of common temporary/disposable email domains to block
    blocked_domains = [
        'tempmail.com', 'throwaway.email', '10minutemail.com', 
        'guerrillamail.com', 'mailinator.com', 'trashmail.com'
    ]
    
    # Extract domain from email
    try:
        domain = value.split('@')[1].lower()
    except IndexError:
        raise ValidationError('Invalid email format')
    
    # Check if domain is in blocked list
    if domain in blocked_domains:
        raise ValidationError(f'Email domain "{domain}" is not allowed')
    
    # Validate domain has at least one dot and valid TLD
    if '.' not in domain:
        raise ValidationError('Email domain must include a valid top-level domain')
    
    # Check for suspicious patterns (multiple dots in a row, special characters)
    if '..' in domain or re.search(r'[^\w.\-]', domain):
        raise ValidationError('Email domain contains invalid characters')
    
    # Ensure domain parts are not empty
    domain_parts = domain.split('.')
    if any(not part for part in domain_parts):
        raise ValidationError('Email domain has invalid structure')

class Team(models.Model):
    id = models.ObjectIdField(primary_key=True, editable=False)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class User(models.Model):
    id = models.ObjectIdField(primary_key=True, editable=False)
    email = models.EmailField(unique=True, validators=[EmailValidator(), validate_email_domain])
    name = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members', db_column='team_id', to_field='id')
    is_superhero = models.BooleanField(default=False)
    
    def clean(self):
        """
        Additional validation for the User model.
        Ensures email is lowercase and validates against malicious patterns.
        """
        super().clean()
        
        if self.email:
            # Normalize email to lowercase
            self.email = self.email.lower().strip()
            
            # Check for excessive length (potential DoS)
            if len(self.email) > 254:  # RFC 5321
                raise ValidationError({'email': 'Email address is too long'})
            
            # Check local part (before @) for suspicious patterns
            try:
                local_part = self.email.split('@')[0]
            except IndexError:
                raise ValidationError({'email': 'Invalid email format'})
            
            # Validate local part length (max 64 chars per RFC 5321)
            if len(local_part) > 64:
                raise ValidationError({'email': 'Email local part is too long'})
            
            # Check for suspicious consecutive special characters
            if re.search(r'[._\-]{2,}', local_part):
                raise ValidationError({'email': 'Email contains suspicious character patterns'})
    
    def save(self, *args, **kwargs):
        """Override save to ensure clean is called"""
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.email

class Activity(models.Model):
    id = models.ObjectIdField(primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities', db_column='user_id', to_field='id')
    type = models.CharField(max_length=100)
    duration = models.IntegerField()  # in minutes
    date = models.DateField()
    
    def __str__(self):
        return f"{self.user.email} - {self.type}"

class Workout(models.Model):
    id = models.ObjectIdField(primary_key=True, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    suggested_for = models.ManyToManyField(User, related_name='suggested_workouts', blank=True)
    
    def __str__(self):
        return self.name

class Leaderboard(models.Model):
    id = models.ObjectIdField(primary_key=True, editable=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='leaderboards', db_column='team_id', to_field='id')
    points = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.team.name} - {self.points} pts"

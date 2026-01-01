#!/usr/bin/env python
"""
Standalone test for email validation without database.
Tests the validation logic directly.
"""
import sys
import os

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'octofit_tracker.settings')

import django
from django.conf import settings

# Override database settings to use SQLite for testing
settings.DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

django.setup()

from django.core.exceptions import ValidationError
from octofit_tracker.models import validate_email_domain, User, Team

def test_validate_email_domain():
    """Test the custom email domain validator"""
    print("Testing email domain validation...")
    
    # Test valid emails
    valid_emails = [
        'user@example.com',
        'user@mail.example.com',
        'user.name@example.com',
        'user+tag@example.com'
    ]
    
    for email in valid_emails:
        try:
            validate_email_domain(email)
            print(f"✓ Valid: {email}")
        except ValidationError as e:
            print(f"✗ Should be valid but failed: {email} - {e}")
            return False
    
    # Test blocked domains
    blocked_emails = [
        'user@tempmail.com',
        'user@mailinator.com',
        'user@throwaway.email',
        'user@10minutemail.com'
    ]
    
    for email in blocked_emails:
        try:
            validate_email_domain(email)
            print(f"✗ Should be blocked but passed: {email}")
            return False
        except ValidationError as e:
            print(f"✓ Correctly blocked: {email}")
    
    # Test invalid patterns
    invalid_emails = [
        'user@localhost',  # No TLD
        'user@example..com',  # Consecutive dots in domain
        'user@.example.com',  # Empty domain part
        'user@example.com.',  # Empty domain part
    ]
    
    for email in invalid_emails:
        try:
            validate_email_domain(email)
            print(f"✗ Should be invalid but passed: {email}")
            return False
        except ValidationError as e:
            print(f"✓ Correctly rejected: {email}")
    
    return True

def test_user_clean_method():
    """Test the User model's clean method (without database operations)"""
    print("\nTesting User model clean method...")
    
    # Test email normalization
    user = User(email='  Test@Example.COM  ', name='Test User')
    user.team_id = None  # Bypass ForeignKey validation for testing
    try:
        user.clean()
        if user.email == 'test@example.com':
            print("✓ Email normalized to lowercase and trimmed")
        else:
            print(f"✗ Email not normalized correctly: {user.email}")
            return False
    except ValidationError as e:
        print(f"✗ Valid email rejected: {e}")
        return False
    
    # Test consecutive special characters in local part
    user = User(email='test..user@example.com', name='Test User')
    user.team_id = None
    try:
        user.clean()
        print(f"✗ Should reject consecutive dots in local part")
        return False
    except ValidationError:
        print("✓ Correctly rejected consecutive dots in local part")
    
    # Test consecutive underscores
    user = User(email='test__user@example.com', name='Test User')
    user.team_id = None
    try:
        user.clean()
        print(f"✗ Should reject consecutive underscores in local part")
        return False
    except ValidationError:
        print("✓ Correctly rejected consecutive underscores in local part")
    
    # Test consecutive dashes
    user = User(email='test--user@example.com', name='Test User')
    user.team_id = None
    try:
        user.clean()
        print(f"✗ Should reject consecutive dashes in local part")
        return False
    except ValidationError:
        print("✓ Correctly rejected consecutive dashes in local part")
    
    # Test email too long
    long_email = 'a' * 250 + '@example.com'
    user = User(email=long_email, name='Test User')
    user.team_id = None
    try:
        user.clean()
        print(f"✗ Should reject excessively long email")
        return False
    except ValidationError:
        print("✓ Correctly rejected excessively long email")
    
    # Test local part too long
    long_local = 'a' * 65 + '@example.com'
    user = User(email=long_local, name='Test User')
    user.team_id = None
    try:
        user.clean()
        print(f"✗ Should reject excessively long local part")
        return False
    except ValidationError:
        print("✓ Correctly rejected excessively long local part")
    
    # Test valid email with single special characters (should pass)
    user = User(email='test.user@example.com', name='Test User')
    user.team_id = None
    try:
        user.clean()
        print("✓ Valid email with single dot in local part accepted")
    except ValidationError as e:
        print(f"✗ Valid email with single dot rejected: {e}")
        return False
    
    user = User(email='test_user@example.com', name='Test User')
    user.team_id = None
    try:
        user.clean()
        print("✓ Valid email with single underscore in local part accepted")
    except ValidationError as e:
        print(f"✗ Valid email with single underscore rejected: {e}")
        return False
    
    user = User(email='test-user@example.com', name='Test User')
    user.team_id = None
    try:
        user.clean()
        print("✓ Valid email with single dash in local part accepted")
    except ValidationError as e:
        print(f"✗ Valid email with single dash rejected: {e}")
        return False
    
    return True

if __name__ == '__main__':
    print("=" * 60)
    print("Email Validation Tests")
    print("=" * 60)
    
    success = True
    
    if not test_validate_email_domain():
        success = False
        print("\n❌ Email domain validation tests FAILED")
    else:
        print("\n✅ Email domain validation tests PASSED")
    
    if not test_user_clean_method():
        success = False
        print("\n❌ User clean method tests FAILED")
    else:
        print("\n✅ User clean method tests PASSED")
    
    print("=" * 60)
    if success:
        print("✅ ALL TESTS PASSED")
        sys.exit(0)
    else:
        print("❌ SOME TESTS FAILED")
        sys.exit(1)

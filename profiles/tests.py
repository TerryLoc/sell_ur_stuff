# profiles/tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import UserProfile
import os.path


class UserProfileTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.profile, created = UserProfile.objects.get_or_create(user=self.user)

    def test_profile_picture_upload(self):
        # Create a dummy image file for testing
        image = SimpleUploadedFile(
            name="test.jpg",
            content=b"file_content",  # Dummy content (simulates file data)
            content_type="image/jpeg",
        )
        self.profile.profile_picture = image
        self.profile.save()
        # Extract the base filename and check if it starts with "test" and ends with ".jpg"
        base_name = os.path.basename(self.profile.profile_picture.name)
        self.assertTrue(base_name.startswith("test") and base_name.endswith(".jpg"))

    def test_profile_string_representation(self):
        self.assertEqual(str(self.profile), f"{self.user.username}'s profile")

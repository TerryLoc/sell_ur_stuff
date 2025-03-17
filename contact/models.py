from django.db import models


# Create your models here.
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)  # For admin to mark as handled

    def __str__(self):
        return f"{self.subject} from {self.name} ({self.email})"

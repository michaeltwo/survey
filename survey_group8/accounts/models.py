from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(
        max_length=10, 
        choices=[('t', 'Survey Taker'), ('c', 'Survey Creator')],
    )

    def __str__(self):
        return self.user.username
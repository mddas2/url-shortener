# models.py in url_shortener app

from django.db import models
from account.models import CustomUser

class ShortenedURL(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    long_url = models.URLField()
    short_key = models.CharField(max_length=10, unique=True)
    click_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.short_key} - {self.long_url}"

from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    description = models.TextField(blank=True)
    date = models.DateTimeField(db_index=True)
    location = models.CharField(max_length=255, db_index=True)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="organized_events")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "title"]
        indexes = [
            models.Index(fields=["date"]),
            models.Index(fields=["location"]),
        ]

    def __str__(self):
        return f"{self.title} @ {self.location}"


class Registration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="registrations")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="registrations")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("event", "user")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} -> {self.event.title}"

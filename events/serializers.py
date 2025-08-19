from rest_framework import serializers
from django.utils import timezone
from .models import Event, Registration


class EventSerializer(serializers.ModelSerializer):
    organizer_username = serializers.ReadOnlyField(source="organizer.username")
    registrations_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Event
        fields = ("id", "title", "description", "date", "location", "organizer",
                  "organizer_username", "registrations_count", "created_at")
        read_only_fields = ("organizer", "organizer_username", "registrations_count", "created_at")

    def validate_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Event date cannot be in the past.")
        return value

    def create(self, validated_data):
        request = self.context["request"]
        validated_data["organizer"] = request.user
        return super().create(validated_data)


class RegistrationSerializer(serializers.ModelSerializer):
    event_title = serializers.ReadOnlyField(source="event.title")
    user_username = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Registration
        fields = ("id", "event", "user", "event_title", "user_username", "created_at")
        read_only_fields = ("user", "event_title", "user_username", "created_at")

    def create(self, validated_data):
        request = self.context["request"]
        validated_data["user"] = request.user
        return super().create(validated_data)

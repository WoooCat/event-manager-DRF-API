from django.db.models import Count
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiResponse


from users.auth import SessionBoundJWTAuthentication
from .models import Event, Registration
from .serializers import EventSerializer, RegistrationSerializer
from .permissions import IsOrganizerOrReadOnly
from .filters import EventFilter


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    filterset_class = EventFilter

    authentication_classes = (SessionBoundJWTAuthentication, )
    permission_classes = [IsOrganizerOrReadOnly]

    search_fields = ["title", "description", "location", "organizer__username"]
    ordering_fields = ["date", "title", "created_at", "registrations_count"]


    def get_queryset(self):
        return (
            Event.objects
            .select_related("organizer")
            .prefetch_related("registrations")
            .annotate(registrations_count=Count("registrations"))
        )

    @extend_schema(
        request=None,
        responses={
            201: OpenApiResponse(description="Registered successfully"),
            400: OpenApiResponse(description="Already registered or capacity exceeded"),
            401: OpenApiResponse(description="Authentication required"),
            404: OpenApiResponse(description="Event not found"),
        },
        summary="Register current user for the event",
        description="Registers the authenticated user for this event.",
    )
    @action(detail=True, methods=["post"], url_path="register", permission_classes=[IsAuthenticated])
    def register(self, request, pk=None):
        event = self.get_object()
        user = request.user

        # idempotent create
        from .models import Registration
        obj, created = Registration.objects.get_or_create(user=user, event=event)
        if not created:
            return Response({"detail": "Already registered."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Registered successfully."}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["get"])
    def attendees(self, request, pk=None):
        event = self.get_object()
        qs = (
            Registration.objects
            .filter(event=event)
            .select_related("user")
            .order_by("-created_at")
        )
        page = self.paginate_queryset(qs)
        ser = RegistrationSerializer(page or qs, many=True)
        if page is not None:
            return self.get_paginated_response(ser.data)
        return Response(ser.data)


class RegistrationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Optional: allow users to review their registrations.
    """
    serializer_class = RegistrationSerializer
    authentication_classes = (SessionBoundJWTAuthentication, )
    permission_classes = (IsAuthenticated, )

    @extend_schema(
        responses={
            200: RegistrationSerializer(many=True),
            401: OpenApiResponse(description="Unauthorized"),
        }
    )
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    def get_queryset(self):
        return (
            Registration.objects
            .select_related("event", "user", "event__organizer")
            .filter(user=self.request.user)
            .order_by("-created_at")
        )

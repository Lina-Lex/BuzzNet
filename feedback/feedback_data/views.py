from django.shortcuts import render

from django.db.models import Q
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)

from rest_framework import generics, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,

)


from . models import FeedForm


from .serializer import (
    CreateFeedBackSerializer,
    FeedBackSerializer
)

# Create your views here.


class CreateFeedbackAPIView(generics.CreateAPIView):
    """
    AN API VIEW THAT GETS THE SERIALIZED DATA FORM
    FROM USER AND SAVES IT TO THE DATABASE.
    """
    serializer_class = CreateFeedBackSerializer


    def get_queryset(self):
        return FeedForm.objects.all()

    def perform_create(self, serializer):
        serializer.save()


class FeedbackListAPIView(generics.ListAPIView):
    """
    AN API THAT QUERY THE DATABASE FOR ALL FEEDBACK
    SAVED TO THE BACKEND
    """

    serializer_class = FeedBackSerializer

    def get_queryset(self):
        return FeedForm.objects.all()

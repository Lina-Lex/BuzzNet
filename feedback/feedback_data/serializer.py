from rest_framework import serializers
from .models import FeedForm



class CreateFeedBackSerializer(serializers.ModelSerializer):
    """
    Uses model form field to serializer user's input
    """

    class Meta:
        model = FeedForm
        fields = "__all__"

    def create(self, validated_data):
        """
        Creates user feedback if all forms are correctly filled(validated)
        """
        return FeedForm.objects.create(**validated_data)


class FeedBackSerializer(serializers.ModelSerializer):
    """
    Display the feedbacks stored in the database ucing the form field allowed 
    """

    class Meta:
        model = FeedForm
        fields = ['full_name', 'feedback', 'created']


from django.db import models

# Create your models here.

class FeedForm(models.Model):
    """
    A model form that takes user's feedback
    """
    feedback = models.TextField(blank= False, null = True)
    phone_contact = models.IntegerField(blank = True, null = True)
    full_name = models.CharField(blank = True, null = True, max_length = 225)
    created = models.DateTimeField(auto_now_add = True)
    
from feedback_data import views
from django.urls import include, path

urlpatterns = [
    path('Feedback/create', views.CreateFeedbackAPIView.as_view()),
    path('feedback', views.FeedbackListAPIView.as_view()),
]

from . import views
from django.urls import path, include

urlpatterns = [
    path('published/<int:id>/', views.survey_results_published, name='survey_delete'),
    ]
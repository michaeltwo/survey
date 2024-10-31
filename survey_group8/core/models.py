from django.db import models
from django.contrib.auth.models import User

#for user and roles, using built-in auth_user table, User

class surveys(models.Model):
    name=models.CharField(max_length=2000)
    description=models.TextField()
    user_id=models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='surveys')
    republished=models.CharField(max_length=100)

class questions(models.Model):
    question_name=models.CharField(max_length=2000)
    survey_id=models.ForeignKey(surveys, on_delete=models.CASCADE, related_name='questions')

class answers(models.Model):
    question_id=models.ForeignKey(questions, on_delete=models.CASCADE, related_name='answers')
    answer=models.TextField()
    type=models.CharField(max_length=10)

class results(models.Model):
    survey_id=models.ForeignKey(surveys, on_delete=models.CASCADE, related_name='results')
    question_id=models.ForeignKey(questions, on_delete=models.CASCADE, related_name='results')
    answer_id=models.ForeignKey(answers, on_delete=models.CASCADE, related_name='results')
    user_id=models.ForeignKey(User, on_delete=models.CASCADE, related_name='results')
    republished_version=models.CharField(max_length=10)

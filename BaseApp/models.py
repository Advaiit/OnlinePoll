from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")
    user_points = models.PositiveIntegerField(default=1)
    profile_pic = models.ImageField(upload_to='profile_pic', blank=True, null=True, default='')

    def __str__(self):
        return self.user.username

class Question(models.Model):
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    question_text = models.CharField(max_length=300, blank=False)
    question_topic = models.CharField(max_length=300, default="Misc")
    question_comments = models.TextField(max_length=500, blank=True)
    responders = models.ManyToManyField(UserProfile, related_name="questions")

    def __str__(self):
        return str(self.question_text)

class Option(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    option_text = models.CharField(max_length=200, blank=False)
    vote_count = models.PositiveIntegerField()

    def __str__(self):
        return str(self.option_text)

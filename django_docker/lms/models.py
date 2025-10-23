from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Inscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='inscriptions')


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(null=True, blank=True)
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='comments')


class Course(models.Model):
    course_id = models.CharField(max_length=50, primary_key=True)
    inscription = models.ForeignKey('Inscription', on_delete=models.CASCADE, related_name='courses_inscription')
    image = models.ImageField(upload_to='courses/')
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE)
    progress = models.FloatField(default=0.0)
    comment = models.ForeignKey('Comment',on_delete=models.CASCADE,related_name='courses_comment')
    role = models.CharField(max_length=50, default='Student')


class Lesson(models.Model):
    unit = models.IntegerField()
    score = models.FloatField()



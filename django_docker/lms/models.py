from django.contrib.auth.models import User
from django.db import models


class Inscription(models.Model):
    """Equivale a Inscriptions del diagrama"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inscriptions')

    def __str__(self):
        return f"Inscription #{self.id} - {self.user.username}"


class Course(models.Model):
    """Course del diagrama"""
    inscription = models.ForeignKey(
        Inscription,
        on_delete=models.CASCADE,
        related_name='courses'
    )
    image = models.ImageField(upload_to='course_images/', null=True, blank=True)
    lesson = models.CharField(max_length=255)
    progress = models.FloatField(default=0.0)
    comment = models.CharField(max_length=255, blank=True)
    role = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.lesson


class Lesson(models.Model):
    """Lesson del diagrama"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    unit = models.IntegerField()
    score = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.course.lesson} - Unit {self.unit}"


class Comment(models.Model):
    """Comments del diagrama"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='comments')
    comment = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username} - {self.course.lesson}"

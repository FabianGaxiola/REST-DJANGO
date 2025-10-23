from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Inscription, Comment, Course, Lesson


class UserSerializer(serializers.ModelSerializer):
    """Serializer for Django User model"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class InscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inscription
        fields = ['id', 'user', 'course']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['comment_id', 'user', 'comment', 'course']

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'unit', 'score']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            'course_id',
            'inscription',
            'image',
            'lesson',
            'progress',
            'comment',
            'role',
        ]
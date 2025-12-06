from django.contrib import admin
from .models import Inscription, Course, Lesson, Comment

admin.site.register(Inscription)
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Comment)

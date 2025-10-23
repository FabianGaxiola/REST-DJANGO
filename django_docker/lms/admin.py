from django.contrib import admin

# Register your models here.
from .models import Inscription, Comment, Course, Lesson


admin.site.register(Inscription)
admin.site.register(Comment)
admin.site.register(Course)
admin.site.register(Lesson)
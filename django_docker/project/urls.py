from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from lms import views as lms_views
from lms.views import (
    UserViewSet,
    InscriptionViewSet,
    CourseViewSet,
    LessonViewSet,
    CommentViewSet,
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'inscriptions', InscriptionViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'lessons', LessonViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('register/', lms_views.register, name='register'),
    path('activate/<uidb64>/<token>/', lms_views.activate_account, name='activate'),
    path('', lms_views.home, name='home'),
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('courses/', lms_views.course_list, name='course_list'),
    path('courses/<int:pk>/', lms_views.course_detail, name='course_detail'),
    path('my-courses/', lms_views.my_courses, name='my_courses'),
    path('accounts/', include('allauth.urls')),
]

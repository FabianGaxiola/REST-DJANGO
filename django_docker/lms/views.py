from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .models import Inscription, Course, Lesson, Comment
from .serializers import (
    UserSerializer,
    InscriptionSerializer,
    CourseSerializer,
    LessonSerializer,
    CommentSerializer,
)


token_generator = PasswordResetTokenGenerator()


def home(request):
    return render(request, "index.html")


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Ese email ya está registrado.")
            return redirect("register")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_active=False,          # se activa solo con el enlace
        )

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)
        activation_link = request.build_absolute_uri(
            f"/activate/{uid}/{token}/"
        )

        subject = "Activa tu cuenta"
        message = f"Hola {user.username},\n\nActiva tu cuenta entrando a este enlace:\n{activation_link}"
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
        )

        messages.success(
            request,
            "Te enviamos un correo con el enlace de activación."
        )
        return redirect("course_list")

    return render(request, "lms/register.html")


def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError, OverflowError):
        user = None

    if user is not None and token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Tu cuenta ha sido activada. Ya puedes iniciar sesión.")
        return redirect("account_login")  # login de allauth
    else:
        return HttpResponse("Enlace de activación no válido o expirado.", status=400)


def course_list(request):
    courses = Course.objects.all()
    return render(request, "lms/course_list.html", {"courses": courses})


def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    lessons = course.lessons.all()
    return render(request, "lms/course_detail.html", {
        "course": course,
        "lessons": lessons,
    })


@login_required
def my_courses(request):
    courses = Course.objects.filter(inscription__user=request.user)
    return render(request, "lms/my_courses.html", {"courses": courses})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class InscriptionViewSet(viewsets.ModelViewSet):
    queryset = Inscription.objects.all()
    serializer_class = InscriptionSerializer
    permission_classes = [IsAuthenticated]


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

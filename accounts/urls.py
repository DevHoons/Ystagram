from django.urls import path
from django.contrib.auth import views as auth_view
from . import views

urlpatterns = [
    path("login/", auth_view.LoginView.as_view(), name="login"),
    path(
        "logout/",
        auth_view.LogoutView.as_view(template_name="registration/logout.html"),
        name="logout",
    ),
    path("signup/", views.signup, name="signup"),
]

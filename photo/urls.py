from django.urls import path
from django.views.generic.detail import DetailView
from . import views
from .models import Photo

app_name = "photo"

urlpatterns = [
    path("", views.photo_list, name="photo_list"),
    path(
        "detail/<int:pk>/",
        DetailView.as_view(model=Photo, template_name="detail.html"),
        name="photo_detail",
    ),
    path("upload/", views.PhotoUploadView.as_view(), name="photo_upload"),
    path("delete/<int:pk>/", views.PhotoDeleteView.as_view(), name="photo_delete"),
    path("update/<int:pk>/", views.PhotoUpdateView.as_view(), name="photo_update"),
]

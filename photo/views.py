from django.shortcuts import render
from .models import Photo


def photo_list(request):
    photos = Photo.objects.all()
    ctx = {"photos": photos}
    return render(request, "list.html", ctx)

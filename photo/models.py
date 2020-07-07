from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Photo(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_photos")
    photo = models.ImageField(upload_to="img/%Y/%m/%d", default="img/no_img.png")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return self.name.username + " " + self.created_at.strftime("%Y-%m-%d %H:%M:%S")

    def get_absolute_url(self):
        return reverse("photo:photo_detail", args=[self.id])

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import Photo


@login_required
def photo_list(request):
    photos = Photo.objects.all()
    ctx = {"photos": photos}
    return render(request, "list.html", ctx)


class PhotoUploadView(LoginRequiredMixin, CreateView):
    model = Photo
    fields = ["photo", "text"]
    template_name = "upload.html"

    def form_valid(self, form):
        form.instance.name_id = self.request.user.id
        if form.is_valid():
            form.instance.save()
            return redirect("/")
        else:
            return self.render_to_response({"form": form})


class PhotoDeleteView(LoginRequiredMixin, DeleteView):
    model = Photo
    success_url = "/"
    template_name = "delete.html"


class PhotoUpdateView(LoginRequiredMixin, UpdateView):
    model = Photo
    fields = ["photo", "text"]
    template_name = "update.html"

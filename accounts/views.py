from django.shortcuts import render
from .forms import SignUpForm


def signup(request):
    if request.method == "POST":
        user_form = SignUpForm(request.POST)
        if user_form.is_valid():
            create_user = user_form.save(commit=False)
            create_user.set_password(user_form.cleaned_data["password"])
            create_user.save()
            return render(
                request, "registration/signup_done.html", {"create_user": create_user}
            )
    else:
        user_form = SignUpForm()

    return render(request, "registration/signup.html", {"form": user_form})

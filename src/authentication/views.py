from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUp


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password")
            return redirect("home")
    else:
        return render(request, "authentication/login.html")


def user_signup(request):
    if request.method == "POST":
        signup_form = SignUp(request.POST)

        if signup_form.is_valid():
            signup_form.save()

            username = signup_form.cleaned_data["username"]
            password = signup_form.cleaned_data["password1"]

            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, "Successfully Signed Up")
            return redirect("home")
        else:
            return render(request, "calculator/home.html")

    else:
        signup_form = SignUp()
        return render(request, "authentication/signup.html", {"signup_form": signup_form})


def user_logout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect("home")

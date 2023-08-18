import requests
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.conf import settings
from .forms import UsForm, MetricForm, SignUp
from calculator.models import UserStat


def landing_page(request):
    metric_form = MetricForm()
    imperial_form = UsForm()
    signup_form = SignUp()

    if request.user.is_authenticated:
        try:
            has_instance = UserStat.objects.get(user=request.user)
        except UserStat.DoesNotExist:
            has_instance = None
    else:
        has_instance = None

    context = {
        "metric_form": metric_form,
        "imperial_form": imperial_form,
        "signup_form": signup_form,
        "has_instance": has_instance,
    }

    return render(request, "calculator/home.html", context)


def metric(request):
    return calculate_macros(request, MetricForm)


def imperial(request):
    return calculate_macros(request, UsForm)


def calculate_macros(request, form_choice):
    if request.method == "POST":
        form = form_choice(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)

            if request.user.is_authenticated:
                instance.user = request.user
                instance.save()

            url = "https://fitness-calculator.p.rapidapi.com/macrocalculator"

            headers = {
                "X-RapidAPI-Key": settings.API_KEY,
                "X-RapidAPI-Host": "fitness-calculator.p.rapidapi.com",
            }

            params = {
                "age": form.cleaned_data["age"],
                "gender": form.cleaned_data["sex"],
                "weight": form.cleaned_data["weight_kg"],
                "height": form.cleaned_data["height_cm"],
                "activitylevel": form.cleaned_data["activity_level"],
                "goal": form.cleaned_data["weight_goal"],
            }

            try:
                response = requests.get(url, headers=headers, params=params)
                response_data = response.json()
                response_data = response_data['data']

                return render(request, "calculator/result.html", {"response_data": response_data})

            except requests.exceptions.RequestException as e:
                error_message = str(e)
                return render(
                    request, "calculator/error.html", {"error_message": error_message}
                )

    else:
        form = form_choice()

    context = {"form": form}

    return render(request, "calculator/home.html", context)


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
            return redirect("macrocal")
    else:
        signup_form = SignUp()
        return render(request, "calculator/home.html", {"signup_form": signup_form})


def user_logout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect("home")

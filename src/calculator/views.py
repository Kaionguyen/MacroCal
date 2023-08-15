import requests
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.conf import settings
from .forms import UsForm, MetricForm, SignUp
from calculator.models import UserStat


def landing_page(request):
    metric_form = MetricForm()
    us_form = UsForm()
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
        "us_form": us_form,
        "signup_form": signup_form,
        "has_instance": has_instance,
    }

    return render(request, "calculator/home.html", context)


def macro_cal(request):
    metric_form = MetricForm(request.POST or None)
    us_form = UsForm(request.POST or None)

    if request.method == "POST":
        if metric_form.is_valid() and "metric-form-submit" in request.POST:
            age = metric_form.cleaned_data["age"]
            sex = metric_form.cleaned_data["sex"]
            weight_kg = metric_form.cleaned_data["weight_kg"]
            height_cm = metric_form.cleaned_data["height_cm"]
            activity_level = metric_form.cleaned_data["activity_level"]
            weight_goal = metric_form.cleaned_data["weight_goal"]

            instance = metric_form.save(commit=False)

            if request.user.is_authenticated:
                instance.user = request.user
                instance.save()

            url = "https://fitness-calculator.p.rapidapi.com/macrocalculator"

            headers = {
                "X-RapidAPI-Key": settings.API_KEY,
                "X-RapidAPI-Host": "fitness-calculator.p.rapidapi.com",
            }

            params = {

                "age": age,
                "gender": sex,
                "weight": weight_kg,
                "height": height_cm,
                "activitylevel": activity_level,
                "goal": weight_goal,
            }

            try:
                response = requests.get(url, headers=headers, params=params)
                response_data = response.json()

                return render(request, "calculator/result.html", {"response_data": response_data})

            except requests.exceptions.RequestException as e:
                error_message = str(e)
                return render(
                    request, "calculator/error.html", {"error_message": error_message}
                )

        elif us_form.is_valid() and "us-form-submit" in request.POST:
            age = us_form.cleaned_data["age"]
            sex = us_form.cleaned_data["sex"]
            weight_kg = us_form.cleaned_data["weight_kg"]
            height_cm = us_form.cleaned_data["height_cm"]
            activity_level = us_form.cleaned_data["activity_level"]
            weight_goal = us_form.cleaned_data["weight_goal"]

            instance = us_form.save(commit=False)

            if request.user.is_authenticated:
                instance.user = request.user
                instance.save()

            url = "https://fitness-calculator.p.rapidapi.com/macrocalculator"

            headers = {
                "X-RapidAPI-Key": settings.API_KEY,
                "X-RapidAPI-Host": "fitness-calculator.p.rapidapi.com",
            }

            params = {
                "age": age,
                "gender": sex,
                "weight": weight_kg,
                "height": height_cm,
                "activitylevel": activity_level,
                "goal": weight_goal,
            }

            try:
                response = requests.get(url, headers=headers, params=params)
                response_data = response.json()

                return render(request, "calculator/result.html", {"response_data": response_data})

            except requests.exceptions.RequestException as e:
                error_message = str(e)
                return render(
                    request, "calculator/error.html", {"error_message": error_message}
                )
    else:
        metric_form = MetricForm()
        us_form = UsForm()

        context = {
            "metric_form": metric_form,
            "us_form": us_form,
        }

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

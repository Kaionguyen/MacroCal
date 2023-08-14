import requests
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.conf import settings
from .forms import MacroCal, SignUp


def landing_page(request):
    macrocal_form = MacroCal()
    signup_form = SignUp()

    context = {
        "macrocal_form": macrocal_form,
        "signup_form": signup_form,
    }

    return render(request, "calculator/base.html", context)


def macro_cal(request):
    if request.method == "POST":
        macrocal_form = MacroCal(request.POST)

        if macrocal_form.is_valid():
            age = macrocal_form.cleaned_data["age"]
            sex = macrocal_form.cleaned_data["sex"]
            activity_level = macrocal_form.cleaned_data["activity_level"]
            weight_goal = macrocal_form.cleaned_data["weight_goal"]

            params = {
                "age": age,
                "gender": sex,
                "activitylevel": activity_level,
                "goal": weight_goal,
            }

            if (
                macrocal_form.cleaned_data["weight_kg"] is not None
                and macrocal_form.cleaned_data["height_cm"] is not None
            ):
                weight_kg = macrocal_form.cleaned_data["weight_kg"]
                height_cm = macrocal_form.cleaned_data["height_cm"]

                params["weight"] = weight_kg
                params["height"] = height_cm

            elif (
                macrocal_form.cleaned_data["weight_lb"] is not None
                and macrocal_form.cleaned_data["height_ft"] is not None
                and macrocal_form.cleaned_data["height_in"] is not None
            ):
                weight_lb = macrocal_form.cleaned_data["weight_lb"]
                height_ft = macrocal_form.cleaned_data["height_ft"]
                height_in = macrocal_form.cleaned_data["height_in"]

                weight_kg = float(weight_lb) * 0.453592
                height_cm = (height_ft * 12 + float(height_in)) * 2.54

                params["weight"] = weight_kg
                params["height"] = height_cm

            else:
                return render(
                    request,
                    "calculator/error.html",
                    {"error_message": "Invalid macrocal_form data."},
                )

            url = "https://fitness-calculator.p.rapidapi.com/macrocalculator"

            headers = {
                "X-RapidAPI-Key": settings.API_KEY,
                "X-RapidAPI-Host": "fitness-calculator.p.rapidapi.com",
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
        macrocal_form = MacroCal()
        return render(request, "calculator/base.html", {"macrocal_form": macrocal_form})


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
            return redirect("home")
    else:
        signup_form = SignUp()
        return render(request, "calculator/base.html", {"signup_form": signup_form})


def user_logout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect("home")

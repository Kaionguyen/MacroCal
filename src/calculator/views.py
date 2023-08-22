import requests
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.conf import settings
from .forms import ImperialForm, MetricForm, SignUp
from calculator.models import UserStat, Diet, MacroDistribution


def landing_page(request):
    metric_form = MetricForm()
    imperial_form = ImperialForm()
    signup_form = SignUp()

    if request.user.is_authenticated:
        try:
            stat_instance = UserStat.objects.get(user=request.user)
        except UserStat.DoesNotExist:
            stat_instance = None
    else:
        stat_instance = None

    context = {
        "metric_form": metric_form,
        "imperial_form": imperial_form,
        "signup_form": signup_form,
    }

    if stat_instance:
        return redirect("profile", pk=stat_instance.pk)
    else:
        return render(request, "calculator/home.html", context)


def profile(request, pk):
    user_stat = UserStat.objects.get(pk=pk)
    diet = Diet.objects.get(stats=user_stat)
    macros = MacroDistribution.objects.filter(user_diet=diet)
    macros = {
        "balanced": macros[0],
        "lowcarbs": macros[1],
        "lowfat": macros[2],
        "highprotein": macros[3],
    }
    return render(request, "calculator/profile.html", {"macros": macros})


def metric(request):
    return calculate_macros(request, MetricForm)


def imperial(request):
    return calculate_macros(request, ImperialForm)


def calculate_macros(request, form_choice):
    if request.method == "POST":
        form = form_choice(request.POST)

        if form.is_valid():
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

                if request.user.is_authenticated:
                    user_stat = form.save(commit=False)
                    user_stat.user = request.user
                    user_stat.save()

                    balanced_data = response_data['balanced']
                    lowcarb_data = response_data['lowcarbs']
                    lowfat_data = response_data['lowfat']
                    highprotein_data = response_data['highprotein']

                    diet = Diet.objects.create(
                        calorie=response_data['calorie'],
                        stats=user_stat,
                    )

                    macros = {
                        "balanced": MacroDistribution.objects.create(plan_name='Balanced', **balanced_data, user_diet=diet),
                        "lowcarbs": MacroDistribution.objects.create(plan_name='Low Carb', **lowcarb_data, user_diet=diet),
                        "lowfat": MacroDistribution.objects.create(plan_name='Low Fat', **lowfat_data, user_diet=diet),
                        "highprotein": MacroDistribution.objects.create(plan_name='High Protein', **highprotein_data, user_diet=diet),
                    }

                    return render(request, "calculator/profile.html", {"macros": macros})
                else:
                    return render(request, "calculator/profile.html", {"macros": response_data})

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
    else:
        return render(request, "calculator/login.html")


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
        return render(request, "calculator/signup.html", {"signup_form": signup_form})


def user_logout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect("home")

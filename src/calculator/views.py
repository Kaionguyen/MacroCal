import requests
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.conf import settings
from .forms import ImperialForm, MetricForm, SignUp
from calculator.models import UserStat, Diet, MacroDistribution


def retrieve_macros(form_data):
    url = "https://fitness-calculator.p.rapidapi.com/macrocalculator"
    headers = {
        "X-RapidAPI-Key": settings.API_KEY,
        "X-RapidAPI-Host": "fitness-calculator.p.rapidapi.com",
    }
    response = requests.get(url, headers=headers, params=form_data)
    response_data = response.json()["data"]
    return response_data


def calculate_macros(request, form_choice):
    if request.method == "POST":
        user = request.user
        authenticated = user.is_authenticated
        stat_instance = None

        if authenticated:
            try:
                stat_instance = UserStat.objects.get(user=request.user)
            except UserStat.DoesNotExist:
                pass

        form = form_choice(request.POST, instance=stat_instance) if stat_instance and authenticated else form_choice(request.POST)

        if form.is_valid():
            form_data = {
                "age": form.cleaned_data["age"],
                "gender": form.cleaned_data["sex"],
                "weight": form.cleaned_data["weight_kg"],
                "height": form.cleaned_data["height_cm"],
                "activitylevel": form.cleaned_data["activity_level"],
                "goal": form.cleaned_data["weight_goal"],
            }

            try:
                response_data = retrieve_macros(form_data)

                balanced_data = response_data['balanced']
                lowcarb_data = response_data['lowcarbs']
                lowfat_data = response_data['lowfat']
                highprotein_data = response_data['highprotein']

                if not authenticated:
                    form_type = request.POST.get("form_type")

                    if form_type == "metric":
                        metric_form = form
                        imperial_form = ImperialForm()
                    elif form_type == "imperial":
                        imperial_form = form
                        metric_form = MetricForm()
                    else:
                        metric_form = MetricForm()
                        imperial_form = ImperialForm()

                    context = {
                        "form_type": form_type,
                        "macros": response_data,
                        "metric_form": metric_form,
                        "imperial_form": imperial_form,
                    }

                    return render(request, "calculator/profile.html", context)

                elif authenticated and stat_instance:
                    stat_instance = form.save()
                    diet = Diet.objects.get(stats=stat_instance)
                    diet.calorie = round(response_data['calorie'])
                    diet.save(update_fields=['calorie'])

                    macro_names = ['balanced', 'lowcarbs', 'lowfat', 'highprotein']
                    macro_distribution = MacroDistribution.objects.filter(user_diet=diet)

                    for i, macro in enumerate(macro_distribution):
                        data = response_data[macro_names[i]]
                        macro.protein = round(data['protein'])
                        macro.carbs = round(data['carbs'])
                        macro.fat = round(data['fat'])
                        macro.save(update_fields=['protein', 'carbs', 'fat'])

                    macros = {
                        "calorie": diet.calorie,
                        "balanced": MacroDistribution.objects.get(plan_name='Balanced', user_diet=diet),
                        "lowcarbs": MacroDistribution.objects.get(plan_name='Low Carb', user_diet=diet),
                        "lowfat": MacroDistribution.objects.get(plan_name='Low Fat', user_diet=diet),
                        "highprotein": MacroDistribution.objects.get(plan_name='High Protein', user_diet=diet),
                    }

                else:
                    stat_instance = form.save(commit=False)
                    stat_instance.user = user
                    stat_instance.save()

                    diet = Diet.objects.create(
                        calorie=round(response_data['calorie']),
                        stats=stat_instance,
                    )

                    macros = {
                        "calorie": response_data['calorie'],
                        "balanced": MacroDistribution.objects.create(plan_name='Balanced', **balanced_data, user_diet=diet),
                        "lowcarbs": MacroDistribution.objects.create(plan_name='Low Carb', **lowcarb_data, user_diet=diet),
                        "lowfat": MacroDistribution.objects.create(plan_name='Low Fat', **lowfat_data, user_diet=diet),
                        "highprotein": MacroDistribution.objects.create(plan_name='High Protein', **highprotein_data, user_diet=diet),
                    }

                return render(request, "calculator/profile.html", {"macros": macros})

            except requests.exceptions.RequestException as e:
                error_message = str(e)
                return render(
                    request, "calculator/error.html", {"error_message": error_message}
                )

    else:
        form = form_choice()
        context = {"form": form}

        return render(request, "calculator/home.html", context)


def landing_page(request):
    metric_form = MetricForm()
    imperial_form = ImperialForm()
    signup_form = SignUp()

    if request.user.is_authenticated:
        try:
            stat_instance = UserStat.objects.get(user=request.user)
            return redirect("profile", pk=stat_instance.pk)
        except UserStat.DoesNotExist:
            pass

    context = {
        "metric_form": metric_form,
        "imperial_form": imperial_form,
        "signup_form": signup_form,
    }

    return render(request, "calculator/home.html", context)


def profile(request, pk):
    user_stat = UserStat.objects.get(pk=pk)
    diet = Diet.objects.get(stats=user_stat)
    macros = MacroDistribution.objects.filter(user_diet=diet)
    macros = {
        "calorie": diet.calorie,
        "balanced": macros[0],
        "lowcarbs": macros[1],
        "lowfat": macros[2],
        "highprotein": macros[3],
    }
    return render(request, "calculator/profile.html", {"macros": macros})


def edit_profile(request, pk):
    current_record = UserStat.objects.get(pk=pk)
    metric_form = MetricForm(request.POST or None, instance=current_record)
    imperial_form = ImperialForm(request.POST or None, instance=current_record)

    return render(request, "calculator/edit_profile.html", {"metric_form": metric_form, "imperial_form": imperial_form})


def metric(request):
    return calculate_macros(request, MetricForm)


def imperial(request):
    return calculate_macros(request, ImperialForm)


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

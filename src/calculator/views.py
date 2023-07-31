import requests
from django.shortcuts import render
from django.conf import settings
from .forms import UserInfo


def nutrition_data(request):
    form = UserInfo()

    if request.method == 'POST':
        form = UserInfo(request.POST)

        if form.is_valid():
            age = form.cleaned_data['age']
            sex = form.cleaned_data['sex']
            weight_kg = form.cleaned_data['weight_kg']
            height_cm = form.cleaned_data['height_cm']
            activity_level = form.cleaned_data['activity_level']
            weight_goal = form.cleaned_data['weight_goal']

            url = 'https://fitness-calculator.p.rapidapi.com/macrocalculator'

            headers = {
                "X-RapidAPI-Key": settings.API_KEY,
                "X-RapidAPI-Host": "fitness-calculator.p.rapidapi.com"
            }

            params = {
                'age': age,
                'gender': sex,
                'weight': weight_kg,
                'height': height_cm,
                'activitylevel': activity_level,
                'goal': weight_goal,
            }

            try:
                response = requests.get(url, headers=headers, params=params)
                response_data = response.json()

                calories = round(response_data['data']['calorie'])

                return render(request, 'calculator/result.html', {'calories': calories})

            except requests.exceptions.RequestException as e:
                error_message = str(e)
                return render(request, 'calculator/error.html', {'error_message': error_message})

    return render(request, 'calculator/index.html', {'form': form})

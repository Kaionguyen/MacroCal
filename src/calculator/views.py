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
            activity_level = form.cleaned_data['activity_level']
            weight_goal = form.cleaned_data['weight_goal']

            params = {
                'age': age,
                'gender': sex,
                'activitylevel': activity_level,
                'goal': weight_goal,
            }

            if form.cleaned_data['weight_kg'] is not None and form.cleaned_data['height_cm'] is not None:
                weight_kg = form.cleaned_data['weight_kg']
                height_cm = form.cleaned_data['height_cm']

                params['weight'] = weight_kg
                params['height'] = height_cm

            elif form.cleaned_data['weight_lb'] is not None and form.cleaned_data['height_ft'] is not None and form.cleaned_data['height_in'] is not None:
                weight_lb = form.cleaned_data['weight_lb']
                height_ft = form.cleaned_data['height_ft']
                height_in = form.cleaned_data['height_in']

                weight_kg = float(weight_lb) * 0.453592
                height_cm = (height_ft * 12 + float(height_in)) * 2.54

                params['weight'] = weight_kg
                params['height'] = height_cm

            else:
                return render(request, 'calculator/error.html', {'error_message': 'Invalid form data.'})

            url = 'https://fitness-calculator.p.rapidapi.com/macrocalculator'

            headers = {
                "X-RapidAPI-Key": settings.API_KEY,
                "X-RapidAPI-Host": "fitness-calculator.p.rapidapi.com"
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

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
            gender = form.cleaned_data['gender']
            weight_kg = form.cleaned_data['weight_kg']
            height_cm = form.cleaned_data['height_cm']
            activity_level = form.cleaned_data['activity_level']

            url = 'https://fitness-calculator.p.rapidapi.com/dailycalorie'

            headers = {
                "X-RapidAPI-Key": settings.API_KEY,
                "X-RapidAPI-Host": "fitness-calculator.p.rapidapi.com"
            }

            params = {
                'age': age,
                'gender': gender,
                'weight_kg': weight_kg,
                'height_cm': height_cm,
                'activitylevel': activity_level,
            }
from decimal import Decimal
from calculator.models import UserStat
from django.forms import ModelForm
from django import forms


class MetricForm(ModelForm):
    age = forms.IntegerField(label='Age', min_value=1, max_value=80)
    weight_kg = forms.DecimalField(label='Weight (kg)', min_value=40, max_value=160, decimal_places=2)
    height_cm = forms.DecimalField(label='Height (cm)', min_value=130, max_value=230, decimal_places=2)

    class Meta:
        model = UserStat
        fields = ('age', 'sex', 'weight_kg', 'height_cm', 'activity_level', 'weight_goal')

    def clean(self):
        cleaned_data = super().clean()

        weight_kg = cleaned_data.get('weight_kg')
        height_cm = cleaned_data.get('height_cm')

        if weight_kg is not None:
            weight_lb = round(weight_kg * Decimal('2.20462'))
            cleaned_data['weight_lb'] = weight_lb

        if height_cm is not None:
            height_ft = int(height_cm // Decimal('30.48'))
            height_in = round((height_cm % Decimal('30.48')) / Decimal('2.54'), 2)
            cleaned_data['height_ft'] = height_ft
            cleaned_data['height_in'] = height_in

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        instance.weight_lb = self.cleaned_data['weight_lb']
        instance.height_ft = self.cleaned_data['height_ft']
        instance.height_in = self.cleaned_data['height_in']

        if commit:
            instance.save()

        return instance


class ImperialForm(ModelForm):
    age = forms.IntegerField(label='Age', min_value=1, max_value=80)
    weight_lb = forms.DecimalField(label='Weight (lb)', min_value=88.18, max_value=352.74, decimal_places=2)
    height_ft = forms.IntegerField(label='Height (ft)', min_value=4, max_value=6)
    height_in = forms.DecimalField(label='Height (in)', min_value=0, max_value=11.99, decimal_places=2)

    class Meta:
        model = UserStat
        fields = ('age', 'sex', 'weight_lb', 'height_ft', 'height_in', 'activity_level', 'weight_goal')

    def clean(self):
        cleaned_data = super().clean()

        weight_lb = cleaned_data.get('weight_lb')
        height_ft = cleaned_data.get('height_ft')
        height_in = cleaned_data.get('height_in')

        if weight_lb is not None:
            weight_kg = round(weight_lb / Decimal('2.20462'), 2)
            cleaned_data['weight_kg'] = weight_kg

        if height_ft is not None and height_in is not None:
            height_cm = round((height_ft * Decimal('30.48')) + (height_in * Decimal('2.54')), 2)
            cleaned_data['height_cm'] = height_cm

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        instance.weight_kg = self.cleaned_data['weight_kg']
        instance.height_cm = self.cleaned_data['height_cm']

        if commit:
            instance.save()

        return instance

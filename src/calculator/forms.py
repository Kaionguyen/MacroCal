from decimal import Decimal
from django.contrib.auth.models import User
from calculator.models import UserStat
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django import forms


class MetricForm(ModelForm):
    class Meta:
        model = UserStat
        fields = ('age', 'sex', 'weight_kg', 'height_cm', 'activity_level', 'weight_goal')

    def clean(self):
        cleaned_data = super().clean()

        weight_kg = cleaned_data.get('weight_kg')
        height_cm = cleaned_data.get('height_cm')

        if weight_kg is not None:
            weight_lb = round(weight_kg * Decimal('2.20462'), 2)
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


class SignUp(UserCreationForm):
    email = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
    first_name = forms.CharField(label='', max_length=30, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(label='', max_length=30, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUp, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'

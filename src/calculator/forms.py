from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms


class UserInfo(forms.Form):
    age = forms.IntegerField(label='Age', min_value=0, max_value=80)
    sex = forms.ChoiceField(label='Sex', choices=[('male', 'Male'), ('female', 'Female')])
    weight_kg = forms.DecimalField(label='Weight (kg)', min_value=40, max_value=160, required=False)
    height_cm = forms.DecimalField(label='Height (cm)', min_value=130, max_value=230, required=False)
    weight_lb = forms.DecimalField(label='Weight (lb)', min_value=88.2, max_value=352.7, required=False)
    height_ft = forms.IntegerField(label='Height (ft)', min_value=4, max_value=7, required=False)
    height_in = forms.DecimalField(label='Height (in)', min_value=0, max_value=12.00, required=False)
    activity_level = forms.ChoiceField(
        label='Activity Level',
        choices=[
            ('1', 'BMR'),
            ('2', 'Sedentary: little or no exercise'),
            ('3', 'Exercise 1-3 times/week'),
            ('4', 'Exercise 4-5 times/week'),
            ('5', 'Daily exercise or intense exercise 3-4 times/week'),
            ('6', 'Intense exercise 6-7 times/week'),
            ('7', 'Very intense exercise daily, or physical job')])

    weight_goal = forms.ChoiceField(
        label='Weight Goal',
        choices=[
            ('maintain', 'Maintain weight'),
            ('mildlose', 'Mild weight loss'),
            ('weightlose', 'Weight loss'),
            ('extremelose', 'Extreme weight loss'),
            ('mildgain', 'Mild weight gain'),
            ('weightgain', 'Weight gain'),
            ('extremegain', 'Extreme weight gain')])


class SignUp(UserCreationForm):
    email = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
    first_name = forms.CharField(label='', max_length=30, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(label='', max_length=30, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))

    class Meta:
        model = User
        feilds = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUp, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
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

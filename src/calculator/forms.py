from django import forms


class UserInfo(forms.Form):
    age = forms.IntegerField(label='Age', min_value=0, max_value=80)
    gender = forms.ChoiceField(label='Gender', choices=[('male', 'Male'), ('female', 'Female')])
    weight_kg = forms.DecimalField(label='Weight (kg)', min_value=40, max_value=160)
    height_cm = forms.DecimalField(label='Height (cm)', min_value=130, max_value=230)
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

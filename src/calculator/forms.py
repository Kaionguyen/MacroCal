from django import forms


class UserInfo(forms.Form):
    age = forms.IntegerField(label='Age', min_value=0)
    gender = forms.ChoiceField(label='Gender', choices=[('male', 'Male'), ('female', 'Female')])
    weight_kg = forms.DecimalField(label='Weight (kg)', min_value=0)
    height_cm = forms.DecimalField(label='Height (cm)', min_value=0)
    activity_level = forms.ChoiceField(
        label='Activity Level',
        choices=[
            ('level_1', 'Sedentary: little or no exercise'),
            ('level_2', 'Exercise 1-3 times/week'),
            ('level_3', 'Exercise 4-5 times/week'),
            ('level_4', 'Daily exercise or intense exercise 3-4 times/week'),
            ('level_5', 'Intense exercise 6-7 times/week'),
            ('level_6', 'Very intense exercise daily, or physical job')])

    # weight_goal = forms.ChoiceField(
    #     label='Weight Goal',
    #     choices=[
    #         ('maintain', 'Maintain weight'),
    #         ('mildlose', 'Mild weight loss'),
    #         ('weightlose', 'Weight loss'),
    #         ('extremelose', 'Extreme weight loss'),
    #         ('mildgain', 'Mild weight gain'),
    #         ('weightgain', 'Weight gain'),
    #         ('extremegain', 'Extreme weight gain')])

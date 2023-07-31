from django import forms


class UserInfo(forms.Form):
    age = forms.IntegerField(label='Age', min_value=0, max_value=80)
    sex = forms.ChoiceField(label='Sex', choices=[('male', 'Male'), ('female', 'Female')])
    weight_kg = forms.DecimalField(label='Weight (kg)', min_value=40, max_value=160)
    height_cm = forms.DecimalField(label='Height (cm)', min_value=130, max_value=230)
    weight_lb = forms.IntegerField(label='Weight (lb)', min_value=88, max_value=352)
    height_ft = forms.IntegerField(label='Height (ft)', min_value=4, max_value=7)
    height_in = forms.DecimalField(label='Height (in)', min_value=3.1811, max_value=6.5512)
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

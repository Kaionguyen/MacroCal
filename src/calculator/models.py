from django.db import models


class UserProfile(models.Model):
    age = models.IntegerField()
    gender = models.CharField(max_length=6, choices=[('male', 'Male'), ('female', 'Female')])
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2)
    height_cm = models.DecimalField(max_digits=5, decimal_places=2)
    activity_level = models.CharField(max_length=1, choices=[
        ('1', 'BMR'),
        ('2', 'Sedentary: little or no exercise'),
        ('3', 'Exercise 1-3 times/week'),
        ('4', 'Exercise 4-5 times/week'),
        ('5', 'Daily exercise or intense exercise 3-4 times/week'),
        ('6', 'Intense exercise 6-7 times/week'),
        ('7', 'Very intense exercise daily, or physical job')
    ])
    weight_goal = models.CharField(max_length=11, choices=[
        ('maintain', 'Maintain weight'),
        ('mildlose', 'Mild weight loss'),
        ('weightlose', 'Weight loss'),
        ('extremelose', 'Extreme weight loss'),
        ('mildgain', 'Mild weight gain'),
        ('weightgain', 'Weight gain'),
        ('extremegain', 'Extreme weight gain')
    ])

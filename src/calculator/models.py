from django.contrib.auth.models import User
from django.db import models


class UserStat(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    sex = models.CharField(max_length=6, choices=[('male', 'Male'), ('female', 'Female')])
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2)
    height_cm = models.DecimalField(max_digits=5, decimal_places=2)
    weight_lb = models.DecimalField(max_digits=5, decimal_places=2)
    height_ft = models.IntegerField()
    height_in = models.DecimalField(max_digits=5, decimal_places=2)
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

    def __str__(self):
        return self.user.get_username()


class Macro(models.Model):
    input_data = models.OneToOneField(UserStat, on_delete=models.CASCADE)
    calorie = models.PositiveIntegerField()
    balanced_protein = models.DecimalField(max_digits=10, decimal_places=2)
    balanced_fat = models.DecimalField(max_digits=10, decimal_places=2)
    balanced_carbs = models.DecimalField(max_digits=10, decimal_places=2)
    lowfat_protein = models.DecimalField(max_digits=10, decimal_places=2)
    lowfat_fat = models.DecimalField(max_digits=10, decimal_places=2)
    lowfat_carbs = models.DecimalField(max_digits=10, decimal_places=2)
    lowcarb_protein = models.DecimalField(max_digits=10, decimal_places=2)
    lowcarb_fat = models.DecimalField(max_digits=10, decimal_places=2)
    lowcarb_carbs = models.DecimalField(max_digits=10, decimal_places=2)
    highprotein_protein = models.DecimalField(max_digits=10, decimal_places=2)
    highprotein_fat = models.DecimalField(max_digits=10, decimal_places=2)
    highprotein_carbs = models.DecimalField(max_digits=10, decimal_places=2)

from django.contrib.auth.models import User
from django.db import models


class MacroDistribution(models.Model):
    protein = models.DecimalField(max_digits=5, decimal_places=2)
    carb = models.DecimalField(max_digits=5, decimal_places=2)
    fat = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Protein: {self.protein}, Carb: {self.carb}, Fat: {self.fat}"


class Diet(models.Model):
    calories = models.PositiveIntegerField()
    balanced = models.OneToOneField(MacroDistribution, on_delete=models.CASCADE, related_name='balanced')
    lowcarb = models.OneToOneField(MacroDistribution, on_delete=models.CASCADE, related_name='lowcarb')
    lowfat = models.OneToOneField(MacroDistribution, on_delete=models.CASCADE, related_name='lowfat')
    highprotein = models.OneToOneField(MacroDistribution, on_delete=models.CASCADE, related_name='highprotein')

    def __str__(self):
        return f"Calories: {self.calories}, Balanced: {self.balanced}, Low Carb: {self.lowcarb}, Low Fat: {self.lowfat}, High Protein: {self.highprotein}"


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
    user_diet = models.ForeignKey(Diet, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.get_username()

from django.contrib.auth.models import User
from django.db import models


class UserStat(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='stats')
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
        return f"{self.user.username}'s Stats (id: {self.user.id})"


class Diet(models.Model):
    calorie = models.PositiveIntegerField()
    stats = models.OneToOneField(UserStat, on_delete=models.CASCADE, default=None, related_name='diet')

    def __str__(self):
        return f"{self.stats.user.username}'s Diet (id: {self.stats.user.id}))"


class MacroDistribution(models.Model):
    plan_name = models.CharField(max_length=11, choices=[
        ('balanced', 'Balanced'),
        ('lowfat', 'Low Fat'),
        ('lowcarbs', 'Low Carbs'),
        ('highprotein', 'High Protein'),
    ], null=True)
    protein = models.DecimalField(max_digits=5, decimal_places=2)
    carbs = models.DecimalField(max_digits=5, decimal_places=2)
    fat = models.DecimalField(max_digits=5, decimal_places=2)
    user_diet = models.ForeignKey(Diet, on_delete=models.CASCADE, default=None, related_name='macro_distribution')

    def __str__(self):
        return f"{self.plan_name} diet (id: {self.user_diet.stats.user.id})"

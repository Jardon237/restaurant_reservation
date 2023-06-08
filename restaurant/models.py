from django.db import models

# Create your models here.

class ReservationSetting(models.Model):
    number_of_tables = models.IntegerField()
    date = models.DateField()
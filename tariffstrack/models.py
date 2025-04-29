from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=2, primary_key=True, unique=True)

    def __str__(self):
        return self.name

class Tariff(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    target_type = models.CharField(max_length=255)
    target = models.CharField(max_length=255)
    first_announced = models.CharField(max_length=255)
    date_in_effect = models.CharField(max_length=255)
    rate = models.FloatField()

    def __str__(self):
         return self.country.name + " - " + self.target_type + " - " + self.target + " - " + str(self.rate*100.00) + "%"

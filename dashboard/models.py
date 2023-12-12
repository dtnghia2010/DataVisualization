from django.db import models


class Add_Data(models.Model):
    country = models.CharField(max_length=100)
    population = models.IntegerField()

    class Meta:
        verbose_name_plural = 'Country Population Data'

    def __str__(self):
        return f'{self.country}-{self.population}'






class Upload_File(models.Model):
    attribute1 = models.CharField(max_length=100, null=True, default=None)
    attribute2 = models.BigIntegerField(null=True, default=None)
def __str__(self):
        return f'{self.attribute1}-{self.atrribute2}'



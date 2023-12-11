from django.db import models


class Add_Data(models.Model):
    country = models.CharField(max_length=100)
    population = models.IntegerField()

    class Meta:
        verbose_name_plural = 'Country Population Data'

    def __str__(self):
        return f'{self.country}-{self.population}'


# models.py
class Upload_File(models.Model):
    file = models.FileField(upload_to='uploads/')
    CountryName = models.CharField(("Country Name"),max_length=255)  # Thêm thuộc tính
    CountryCode = models.CharField(("Country Code"), max_length=255)
    Year_2022 = models.BigIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.CountryName}-{self.CountryCode}-{self.Year_2022}'



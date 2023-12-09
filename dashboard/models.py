from django.db import models


class CountryData(models.Model):
    country = models.CharField(max_length=100)
    population = models.IntegerField()

    class Meta:
        verbose_name_plural = 'Country Population Data'

    def __str__(self):
        return f'{self.country}-{self.population}'


# models.py
class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    attribute1 = models.CharField(("atrribute1"),max_length=255)  # Thêm thuộc tính
    attribute2 = models.CharField(("attribute2"),max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name



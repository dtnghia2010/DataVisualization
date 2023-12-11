from django.db import models


class Add_Data(models.Model):
    country = models.CharField(max_length=100)
    population = models.IntegerField()

    class Meta:
        verbose_name_plural = 'Country Population Data'

    def __str__(self):
        return f'{self.country}-{self.population}'


# models.py
# models.py
from django.db import models

# models.py
from django.db import models

# models.py
from django.db import models

# models.py
from django.db import models

class Upload_File(models.Model):
    document = models.FileField(upload_to='uploads/')
    attribute1 = models.CharField(max_length=255, default='your_default_value')
    attribute2 = models.DecimalField(max_digits=15, decimal_places=2)
    def __str__(self):
        return self.document.name



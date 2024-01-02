# models.py
# models.py
# Name: 1
# Duong Trong Nghia ITITIU21256
# Ngo Thi Thuong ITCSIU21160
# Nguyen Pham Ky Phuong ITITIU21287
# Nguyen Anh Thang ITCSIU21233
# Purpose: Set models for the database.
from django.db import models


class Add_Data(models.Model):
    # Mô hình cho dữ liệu của add_data
    country = models.CharField(max_length=100)
    population = models.IntegerField()

    class Meta:
        verbose_name_plural = 'Country Population Data'

    def to_dict(self):
        return self.__dict__

    def __str__(self):
        return f'{self.country}-{self.population}'


class Upload_File(models.Model):
    # Mô hình cho dữ liệu từ tệp CSV được tải lên
    attribute1 = models.CharField(max_length=100, null=True, default=None)
    attribute2 = models.BigIntegerField(null=True, default=None)

    def to_dict(self):
        return self.__dict__

    def __str__(self):
        return f'{self.attribute1}-{self.attribute2}'

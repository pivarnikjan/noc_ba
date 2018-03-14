from django.db import models


class Hotels(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=10)
    country_name = models.CharField(max_length=100)
    rating = models.CharField(max_length=5)
    price = models.CharField(max_length=8)
    image = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    check_in_date = models.CharField(max_length=20, null=True, blank=True)
    check_out_date = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        db_table = 'hotels'

from django.db import models

# Create your models here.


class Stock(models.Model):
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    # Add more fields as needed, such as stock price, company information, etc.

    def __str__(self):
        return self.symbol  # Customize how the model appears in the admin panel

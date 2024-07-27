from django.db import models


class Restaurant(models.Model):
    restaurant_name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    distance = models.IntegerField()
    rating = models.FloatField()
    avatar = models.ImageField(upload_to='images/restaurant/')

    def __str__(self):
        return self.restaurant_name


class Menu(models.Model):
    menu_name = models.CharField(max_length=100)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menus')
    price = models.IntegerField()
    description = models.TextField()
    buy_count = models.IntegerField()

    def __str__(self):
        return self.menu_name

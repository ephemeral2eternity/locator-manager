from django.db import models

# Create your models here.
class Locator(models.Model):
	name = models.CharField(max_length=200)
	ip = models.CharField(max_length=200)
	location = models.CharField(max_length=200)
	longitude = models.DecimalField(max_digits=10, decimal_places=5)
	latitude = models.DecimalField(max_digits=10, decimal_places=5)

	def __str__(self):
		return str(self.name)

class Cache(models.Model):
	name = models.CharField(max_length=200)
	ip = models.CharField(max_length=200)
	location = models.CharField(max_length=200)
	longitude = models.DecimalField(max_digits=10, decimal_places=5)
	latitude = models.DecimalField(max_digits=10, decimal_places=5)

	def __str__(self):
		return str(self.name)

from django.db import models

# Create your models here.
class GeoConnected(models.Model):
	locator = models.CharField(max_length=100)
	client = models.CharField(max_length=100)
	ip = models.CharField(max_length=100)
	city = models.CharField(max_length=100)
	region = models.CharField(max_length=100)
	country = models.CharField(max_length=100)
	AS = models.CharField(max_length=100)
	ISP = models.CharField(max_length=500)
	longitude = models.DecimalField(max_digits=10, decimal_places=5)
	latitude = models.DecimalField(max_digits=10, decimal_places=5)
	latest_update = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return str(self.client)

class NetConnected(models.Model):
	locator = models.CharField(max_length=100)
	client = models.CharField(max_length=100)
	ip = models.CharField(max_length=100)
	city = models.CharField(max_length=100)
	region = models.CharField(max_length=100)
	country = models.CharField(max_length=100)
	AS = models.CharField(max_length=100)
	ISP = models.CharField(max_length=500)
	longitude = models.DecimalField(max_digits=10, decimal_places=5)
	latitude = models.DecimalField(max_digits=10, decimal_places=5)
	latest_update = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return str(self.client)

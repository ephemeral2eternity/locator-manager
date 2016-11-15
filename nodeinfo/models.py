from django.db import models

# Create your models here.
class Node(models.Model):
    name = models.CharField(max_length=100, default="")
    ip = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=10, default="router")
    city = models.CharField(max_length=100, default="")
    region = models.CharField(max_length=100, default="")
    country = models.CharField(max_length=100, default="")
    AS = models.CharField(max_length=100, default="")
    ISP = models.CharField(max_length=200, default="")
    longitude = models.DecimalField(max_digits=10, decimal_places=5, default=0.0)
    latitude = models.DecimalField(max_digits=10, decimal_places=5, default=0.0)
    latest_check = models.DateTimeField(auto_now=True)

def __str__(self):
    return str(self.name)

class Edge(models.Model):
    src = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='node_source')
    dst = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='node_target')
    latest_check = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["src", "dst"]

    def __str__(self):
        return str(self.src.ip + "<-->" + self.dst.ip)
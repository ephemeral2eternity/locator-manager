from django.db import models

# Create your models here.
class Node(models.Model):
    name = models.CharField(max_length=100)
    ip = models.CharField(max_length=100)
    network_id = models.IntegerField(default=-1)
    type = models.CharField(max_length=100)
    latest_check = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.type + ":" + self.ip

# Network defines a network that several routers in an end-to-end delivery path belongs to
class Network(models.Model):
    type = models.CharField(max_length=100)
    name = models.CharField(max_length=100, default="")
    latitude = models.DecimalField(max_digits=10, decimal_places=4, default=0.0)
    longitude = models.DecimalField(max_digits=10, decimal_places=4, default=0.0)
    ASNumber = models.IntegerField(default=-1)
    nodes = models.ManyToManyField(Node)
    city = models.CharField(max_length=100, default="")
    region = models.CharField(max_length=100, default="")
    country = models.CharField(max_length=100, default="")

    def __str__(self):
        return "Network " + str(self.id) + " AS " + str(self.ASNumber) + " at (" + str(self.latitude) + ", " + str(self.longitude) + ")"

    class Meta:
        index_together = ["ASNumber", "latitude", "longitude"]
        unique_together = ("ASNumber", "latitude", "longitude")

class Session(models.Model):
    src_ip = models.CharField(max_length=100)
    dst_ip = models.CharField(max_length=100)
    route = models.ManyToManyField(Node, through='Hop')
    route_networks = models.ManyToManyField(Network, through='Subnetwork')

    def __str__(self):
        return "Session: " + self.src.name + " <--> " + self.dst.name

# Define hop with its sequence on a client's route
class Hop(models.Model):
    node = models.ForeignKey(Node, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    hopID = models.PositiveIntegerField()

    def __str__(self):
        return str(self.session) + "; Hop #: " + str(self.hopID) + "; Hop name: " + self.node.name

class Subnetwork(models.Model):
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    subnetworkID = models.PositiveIntegerField()

    def __str__(self):
        return str(self.session) + "; Subnetwork #: " + str(self.subnetworkID) + "; Subnetwork name: " + self.network.name

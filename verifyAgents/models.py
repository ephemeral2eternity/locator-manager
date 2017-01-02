from django.db import models

# Node defines a node reported by a pair of verification agents or a video session
class Node(models.Model):
    name = models.CharField(max_length=100)
    ip = models.CharField(max_length=100)
    network_id = models.IntegerField(default=-1)
    type = models.CharField(max_length=100)
    latest_check = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.type + ":" + self.ip

# Edge records the link between two nodes
class Edge(models.Model):
    src = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='node_source')
    dst = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='node_target')
    latest_check = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["src", "dst"]
    def __str__(self):
        return str(self.src.ip + "<-->" + self.dst.ip)

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
    isVideoPath = models.BooleanField(default=False)

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
    isVideoSession = models.BooleanField(default=False)

    def __str__(self):
        if self.isVideoSession:
            return "Video Session: " + self.src_ip + " <--> " + self.dst_ip
        else:
            return "Verification Session: " + self.src_ip + " <--> " + self.dst_ip

class VerifySession(models.Model):
    src_ip = models.CharField(max_length=100)
    dst_ip = models.CharField(max_length=100)
    length = models.IntegerField()
    networks = models.ManyToManyField(Network)

    def __str__(self):
        return "Verification Session : " + self.src_ip + "<-->" + self.dst_ip + ",".join(ntw.id for ntw in self.networks.all())

class NetworkForVerifySession(models.Model):
    network = models.ForeignKey(Network)
    verify_sessions = models.ManyToManyField(Session)

    def __str__(self):
        return str(self.network)

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

    def __str__(self):
        return str(self.session) + "; Subnetwork name: " + self.network.name

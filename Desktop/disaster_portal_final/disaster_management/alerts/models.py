from django.db import models

class Alert(models.Model):
    identifier = models.CharField(max_length=255)
    sender = models.CharField(max_length=255)  # Add other fields as needed
    sent_time = models.DateTimeField()
    status = models.CharField(max_length=100)
    msg_type = models.CharField(max_length=100)
    scope = models.CharField(max_length=100)
    category = models.TextField(null=True)  # Allow null values
    event = models.CharField(max_length=255)
    urgency = models.CharField(max_length=100)
    certainty = models.CharField(max_length=100)
    effective = models.DateTimeField(null=False)  # Effective date and time cannot be null
    onset = models.DateTimeField(null=True)  # Onset date and time can be null
    expires = models.DateTimeField(null=False)  # Expires date and time cannot be null
    headline = models.TextField()
    description = models.TextField(null =True)
    area = models.TextField()
    area_desc = models.TextField(null=True)
    polygon = models.TextField()  # Lat,Lng coordinates as a string
    severity = models.TextField()

    class Meta:
        db_table = "cap_alerts1"  # Use the existing table name

    def __str__(self):
        return self.headline

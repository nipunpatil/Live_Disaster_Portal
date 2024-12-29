from django.db import models

class EmergencyContact(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    service_type = models.CharField(max_length=255)  # e.g., Police, Fire Brigade
    address = models.TextField()

    def __str__(self):
        return f"{self.name} ({self.service_type})"

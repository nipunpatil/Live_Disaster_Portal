from django.db import models

class Shelter(models.Model):
    sr_no = models.AutoField(primary_key=True)  # Unique identifier
    health_facility_name = models.CharField(max_length=255)  # Name of the health facility
    pincode = models.CharField(max_length=10)  # Pincode
    latitude = models.FloatField()  # Latitude of the shelter
    longitude = models.FloatField()  # Longitude of the shelter
    altitude = models.FloatField(null=True, blank=True)  # Altitude of the shelter
    facility_type = models.CharField(max_length=100)  # Type of facility
    state_name = models.CharField(max_length=100)  # State name
    district_name = models.CharField(max_length=100)  # District name
    taluka_name = models.CharField(max_length=100)  # Taluka name

    def __str__(self):
        return self.health_facility_name

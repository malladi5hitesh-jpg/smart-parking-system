from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class ParkingSlot(models.Model):
    slot_number = models.IntegerField(unique=True)
    is_occupied = models.BooleanField(default=False)
    booked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    booked_at = models.DateTimeField(null=True, blank=True)

    def release_if_expired(self):
        if self.booked_at:
            expiry_time = self.booked_at + timedelta(hours=1)  # 🔥 TEST VERSION
            if timezone.now() > expiry_time:
                self.is_occupied = False
                self.booked_by = None
                self.booked_at = None
                self.save()

    def get_expiry_time(self):
        if self.booked_at:
            return self.booked_at + timedelta(minutes=1)
        return None

    def __str__(self):
        return f"Slot {self.slot_number}"
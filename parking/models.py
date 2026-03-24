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
        if self.is_occupied and self.booked_at:
            # 🔥 1 hour duration logic
            if timezone.now() >= self.booked_at + timedelta(hours=1):
                self.is_occupied = False
                self.booked_by = None
                self.booked_at = None
                self.save()

    def __str__(self):
        return f"Slot {self.slot_number}"

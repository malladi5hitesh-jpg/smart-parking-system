from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ParkingSlot
from django.utils import timezone


@login_required
def home(request):
    slots = ParkingSlot.objects.all().order_by('slot_number')

    # Auto release expired slots
    for slot in slots:
        slot.release_if_expired()

    user_booking = ParkingSlot.objects.filter(
        booked_by=request.user,
        is_occupied=True
    ).first()

    return render(request, 'home.html', {
        'slots': slots,
        'user_booking': user_booking
    })


@login_required
def book_slot(request, slot_id):
    slot = ParkingSlot.objects.get(id=slot_id)

    slot.release_if_expired()

    existing_booking = ParkingSlot.objects.filter(
        booked_by=request.user,
        is_occupied=True
    ).exists()

    if not existing_booking and not slot.is_occupied:
        slot.is_occupied = True
        slot.booked_by = request.user
        slot.booked_at = timezone.now()
        slot.save()

    return redirect('home')
from datetime import timedelta
from decimal import Decimal

from django.core.management import BaseCommand
from django.utils import timezone

from CarChargingScheduler.models import User, Car, ChargingSchedule, ChargingSlot


def generate_dummy_data():
    user = User.objects.create(username='Test User')
    car = Car.objects.create(user=user, battery_level=Decimal('0.5'))
    charging_schedule = ChargingSchedule.objects.create(car=car)
    ChargingSlot.objects.create(charging_schedule=charging_schedule,
                                       battery_level_gained=Decimal("0.1"),
                                       start_datetime=timezone.now(),
                                       end_datetime=timezone.now() + timedelta(hours=1))

    ChargingSlot.objects.create(charging_schedule=charging_schedule,
                                       battery_level_gained=Decimal("0.1"),
                                       start_datetime=timezone.now() + timedelta(hours=1),
                                       end_datetime=timezone.now() + timedelta(hours=2))

    ChargingSlot.objects.create(charging_schedule=charging_schedule,
                                       battery_level_gained=Decimal("0.1"),
                                       start_datetime=timezone.now() + timedelta(days=1),
                                       end_datetime=timezone.now() + timedelta(days=1, hours=1))


class Command(BaseCommand):
    help = "Generate dummy data"

    def handle(self, *args, **options):
        generate_dummy_data()

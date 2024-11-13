from django.db.models import Sum
from django.utils import timezone
from decimal import Decimal

from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from CarChargingScheduler.mixins import AeModel


class User(AeModel, AbstractBaseUser):
    username = models.CharField(
        blank=True,
        max_length=50,
        verbose_name="Username",
        help_text="Username for the user",
    )


class Car(AeModel):
    user = models.ForeignKey(to=User, verbose_name='User', help_text='User this car belongs to',
                             on_delete=models.PROTECT)

    battery_level = models.DecimalField(decimal_places=2, max_digits=3, default=0.5,
                                        verbose_name='battery_level_percantage',
                                        help_text='the % capacity remaining in the battery expressed')

    is_at_home = models.BooleanField(default=True, verbose_name='car_is_at_home',
                                     help_text='Is this car at home and connected to the grid')


class ChargingSchedule(AeModel):
    paused_until = models.DateTimeField(null=True, verbose_name='charging_schedule_paused_until',
                                        help_text='When this schedule is paused until')

    car = models.ForeignKey(to=Car, verbose_name='Car', help_text='Car linked to Charging Schedule',
                            on_delete=models.CASCADE)

    @property
    def scheduled_paused(self) -> bool:

        # If it's not set it's not paused
        if not self.paused_until:
            return False

        # If paused_until is in the future it's paused
        elif self.paused_until <= timezone.now():
            return True

        # In all other cases it's not paused
        return False

    @property
    def projected_battery_soc(self):
        if self.scheduled_paused:
            return self.car.battery_level

        if not self.car.is_at_home:
            return self.car.battery_level

        # calculate charging slots
        extra_capacity = Decimal('0.00')
        for slot in self.charging_slots.all():
            extra_capacity += slot.battery_level_gained

        return self.car.battery_level + extra_capacity


class ChargingSlot(AeModel):
    """
    Represents a period of time whereby charging is occurring
    """

    charging_schedule = models.ForeignKey(to=ChargingSchedule, on_delete=models.CASCADE,
                                          related_name='charging_slots',
                                          verbose_name='Charging Schedule',
                                          help_text='Charge schedule containing this charge slot')

    start_datetime = models.DateTimeField(auto_now=False, verbose_name='charge_slot_starts_at',
                                          help_text='When this charge slot starts')
    end_datetime = models.DateTimeField(auto_now=False, verbose_name='charge_slot_ends_at',
                                        help_text='When this charge slot ends')

    is_override_applied = models.BooleanField(default=False, verbose_name='charging_schedule_override_live',
                                              help_text='Has a charging override been set')

    battery_level_gained = models.DecimalField(decimal_places=2, max_digits=3, default=0.5,
                                               verbose_name='battery_level_gained',
                                               help_text='the percentage point increase in battery level gained via this '
                                                         'charging slot')

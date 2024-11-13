from django.db import models

from CarChargingScheduler.mixins import AeModel


class Car(models.Model, AeModel):
    battery_level = models.DecimalField(decimal_places=2, default=0.5, verbose_name='battery_level_percantage',
                                        help_text='the % capacity remaining in the battery')

    is_at_home = models.BooleanField(default=True, verbose_name='car_is_at_home',
                                     help_text='Is this car at home and connected to the grid')


class ChargingSchedule(models.Model, AeModel):
    paused_until = models.DateTimeField(null=True, verbose_name='charging_schedule_paused_until',
                                        help_text='When this schedule is paused until')

    car = models.ForeignKey(to=Car, verbose_name='Car', help_text='Car linked to Charging Schedule')


class ChargingSlot(models.Model, AeModel):
    """
    Represents a period of time whereby charging is occurring
    """

    charging_schedule = models.ForeignKey(to=ChargingSchedule, on_delete=models.CASCADE,
                                          verbose_name='Charging Schedule',
                                          help_text='Charge schedule containing this charge slot')

    start_datetime = models.DateTimeField(auto_now=False, verbose_name='charge_slot_starts_at',
                                          help_text='When this charge slot starts')
    end_datetime = models.DateTimeField(auto_now=False, verbose_name='charge_slot_ends_at',
                                        help_text='When this charge slot ends')

    is_override_applied = models.BooleanField(default=False, verbose_name='charging_schedule_override_live',
                                              help_text='Has a charging override been set')

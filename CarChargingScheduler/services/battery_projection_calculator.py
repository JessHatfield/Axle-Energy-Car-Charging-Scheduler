import datetime
from decimal import Decimal

from django.conf import settings
from django.db.models import QuerySet
from django.utils import timezone

BATTERY_OVERRIDE_DURATION_MINS = 60
BATTERY_OVERRIDE_CHARGE_GAINED = 0.1
CHARGE_TIME_TO_CAPACITY_RATIO = BATTERY_OVERRIDE_CHARGE_GAINED / BATTERY_OVERRIDE_DURATION_MINS


def calculate_override_component(charging_slots: QuerySet, override_applied_at: datetime.datetime) -> Decimal:
    """
    If the override is happening outside of a charge_slot

    return a fixed charge value 0.1

    If the override is happening inside of a charge slot

    calculate minuite overlap

    Multiple 0.1 by the % of mins outside of the overlap

    """

    for slot in charging_slots:

        override_start = override_applied_at
        override_end = override_applied_at + datetime.timedelta(minutes=BATTERY_OVERRIDE_DURATION_MINS)
        # If overrider_start betwee

        # If override starts within a given slot
        if slot.end_datetime >= override_start >= slot.start_datetime:
            override_end = override_end.timestamp()
            slot_end = slot.end_datetime.timestamp()

            mins_of_extra_charging = (override_end - slot_end) / 60
            extra_capacity = CHARGE_TIME_TO_CAPACITY_RATIO * mins_of_extra_charging

            return Decimal(f'{round(extra_capacity, settings.DECIMAL_POINT_PRECISION)}')

        # If override ends within a given slot
        if slot.end_datetime >= override_end >= slot.start_datetime:
            override_end = override_end.timestamp()
            slot_end = slot.end_datetime.timestamp()

            mins_of_extra_charging = (slot_end - override_end) / 60
            extra_capacity = CHARGE_TIME_TO_CAPACITY_RATIO * mins_of_extra_charging

            return Decimal(f'{round(extra_capacity, settings.DECIMAL_POINT_PRECISION)}')

    # If we don't find any overlapping slots then we can return the full charge amount

    return Decimal(f'{BATTERY_OVERRIDE_CHARGE_GAINED}')


def calculate_projected_battery_gain(charging_schedule) -> Decimal:
    if charging_schedule.scheduled_paused:
        return Decimal('0.0')

    if not charging_schedule.car.is_at_home:
        return Decimal('0.0')

    # calculate charging slots
    extra_capacity = Decimal('0.00')
    current_time = timezone.now()

    for slot in charging_schedule.charging_slots.exclude(end_datetime__lte=current_time):

        # If timeslot is partially complete calculate partial capacity
        if slot.end_datetime >= current_time >= slot.start_datetime:
            mins_remaining = (slot.end_datetime.timestamp() - current_time.timestamp()) / 60
            extra_capacity = Decimal(
                f'{round(CHARGE_TIME_TO_CAPACITY_RATIO * mins_remaining, settings.DECIMAL_POINT_PRECISION)}')

        else:
            extra_capacity += slot.battery_level_gained

    if charging_schedule.override_applied_at:
        extra_capacity += calculate_override_component(charging_slots=charging_schedule.charging_slots.all(),
                                                       override_applied_at=charging_schedule.override_applied_at)

    return extra_capacity

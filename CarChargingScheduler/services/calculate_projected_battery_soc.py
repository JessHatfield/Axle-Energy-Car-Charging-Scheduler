import datetime
from decimal import Decimal

from django.db.models import QuerySet

BATTERY_OVERRIDE_DURATION_MINS = 60
BATTERY_OVERRIDE_CHARGE_GAINED = 0.1


def calculate_override_component(charging_slots: QuerySet, override_applied_at: datetime.datetime) -> Decimal:
    """
    If the override is happening outside of a charge_slot

    return a fixed charge value 0.1

    If the override is happening inside of a charge slot

    calculate minuite overlap

    Multiple 0.1 by the % of mins outside of the overlap

    """

    for slot in charging_slots:

        # If override starts within a given slot
        if slot.end_datetime >= override_applied_at >= slot.start_datetime:
            override_end = override_applied_at + datetime.timedelta(hours=1)

            override_end = override_end.timestamp()
            slot_end = slot.end_datetime.timestamp()

            mins_of_extra_charging = (override_end - slot_end) * 60

            extra_capacity = (BATTERY_OVERRIDE_CHARGE_GAINED / BATTERY_OVERRIDE_DURATION_MINS) * mins_of_extra_charging

            return extra_capacity

    # If we don't find any overlapping slots then we can return the full charge amount

    return BATTERY_OVERRIDE_CHARGE_GAINED


def calculate_projected_battery_soc(charging_schedule) -> Decimal:
    if charging_schedule.scheduled_paused:
        return charging_schedule.car.battery_level

    if not charging_schedule.car.is_at_home:
        return charging_schedule.car.battery_level

        # calculate charging slots
    extra_capacity = Decimal('0.00')
    for slot in charging_schedule.charging_slots.all():
        extra_capacity += slot.battery_level_gained

    return charging_schedule.car.battery_level + extra_capacity

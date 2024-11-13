import datetime
from decimal import Decimal

from django.db.models import QuerySet


def calculate_override_component(charging_slots: QuerySet, override_applied_at: datetime.datetime) -> Decimal:
    """
    If the override is happening outside of a charge_slot

    return a fixed charge value 0.1

    If the override is happening inside of a charge slot

    calculate minuite overlap

    Multiple 0.1 by the % of mins outside of the overlap

    """

    pass


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

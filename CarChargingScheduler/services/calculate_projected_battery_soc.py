from decimal import Decimal


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

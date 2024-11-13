from datetime import datetime
from decimal import Decimal

import pytest

from CarChargingScheduler.models import ChargingSlot, ChargingSchedule
from CarChargingScheduler.services.calculate_projected_battery_soc import calculate_override_component

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize('slot_start, slot_end, override_applied_at,expected_battery_gain_from_override', [
    ('05:00 - 02/01/2024 +0000', '06:00 - 02/01/2024 +0000', '04:00 - 02/01/2024 +0000', '0.1'),  # No overlap
    ('05:00 - 02/01/2024 +0000', '06:00 - 02/01/2024 +0000', '05:45 - 02/01/2024 +0000', '0.075')  # Overlap of 15 mins with slot

])
def test_calculate_override_component(car,charging_schedule, slot_start, slot_end, override_applied_at,
                                      expected_battery_gain_from_override):


    ChargingSlot.objects.create(charging_schedule=charging_schedule,
                                start_datetime=datetime.strptime(slot_start, "%H:%M - %d/%m/%Y %z"),
                                end_datetime=datetime.strptime(slot_end, "%H:%M - %d/%m/%Y %z"),
                                battery_level_gained=Decimal('0.1')
                                )

    result = calculate_override_component(charging_slots=charging_schedule.charging_slots.all(),
                                          override_applied_at=datetime.strptime(slot_end, "%H:%M - %d/%m/%Y %z"))

    assert result == expected_battery_gain_from_override

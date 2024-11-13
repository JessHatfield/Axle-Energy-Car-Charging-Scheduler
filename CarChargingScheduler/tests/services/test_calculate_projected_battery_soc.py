from datetime import datetime
from decimal import Decimal

import pytest

from CarChargingScheduler.models import ChargingSlot
from CarChargingScheduler.services.calculate_projected_battery_soc import calculate_override_component

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize('slot_start, slot_end, override_applied_at,expected_battery_gain_from_override', [
     ('05:00 - 02/01/2024', '06:00 - 02/01/2024', '04:00 - 02/01/2024', '0.1')  # No overlap
     ('05:00 - 02/01/2024', '06:00 - 02/01/2024', '05:45 - 02/01/2024', '0.075')  # Overlap of 15 mins with slot

])
def test_calculate_override_component(car, charging_schedule, slot_start, slot_end, override_applied_at,
                                      expected_battery_gain_from_override):
    ChargingSlot.objects.create(charging_schedule=charging_schedule,
                                start_datetime=datetime.strptime(slot_start, '%H:%M - %d/%m/%Y'),
                                end_datetime=datetime.strptime(slot_end, '%H:%M - %d/%m/%Y'),
                                battery_level_gained=Decimal('0.1')
                                )

    result = calculate_override_component(charging_slots=charging_schedule.charging_slots,
                                          override_applied_at=datetime.strptime(override_applied_at,
                                                                                '%H:%M - %d/%m/%Y'))

    assert result == expected_battery_gain_from_override

from datetime import datetime
from decimal import Decimal

import pytest
from django.urls import reverse
from rest_framework import status

from CarChargingScheduler.models import ChargingSlot

pytestmark = pytest.mark.django_db


# Things we need to test


def test_user_can_retrieve_state_of_charge(api_client, car, charging_schedule):
    ChargingSlot.objects.create(charging_schedule=charging_schedule,
                                battery_level_gained=Decimal("0.1"),
                                start_datetime=datetime.strptime('01:00 - 01/01/2024',
                                                                 '%H:%M - %d/%m/%Y'),
                                end_datetime=datetime.strptime('02:00 - 01/01/2024',
                                                               '%H:%M - %d/%m/%Y'))

    url = reverse('charging_schedule', kwargs={'car_ae_id': car.ae_id})
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['projected_battery_soc'] == 0.6


@pytest.mark.parametrize('schedule_start,schedule_end,current_datetime,override_applied,battery_starting_level,'
                         'expected_charge_level',
                         [
                             ('01:00 - 02/01/2024', '02:00 - 02/01/2024', '23:00 - 01/01/2024', True,
                              Decimal('0.5'), Decimal('0.6'))
                         ])
def test_user_can_apply_charge_override_and_see_new_battery_soc(api_client, car, charging_schedule,
                                                                schedule_start,
                                                                schedule_end,
                                                                current_datetime,
                                                                override_applied,
                                                                battery_starting_level,
                                                                expected_charge_level):
    """
    We've got a charging scheduled with two slots

    They could either be charging now or in the future

    When an override is applied, we don't care about the schedule until the override has finished

    We assume that an override will always apply 10% of capacity within a 60 min slot

    Scenario 1

    No charge slot active + override applied
        Expected result: 60 mins worth of charge applied to projected_battery soc


    Scenario 2

    1 hr Charge slot active + override applied over same time period

        Expected result: 60 mins worth of charge applied to the project_battery soc

    """

    car.battery_level = battery_starting_level
    car.save()

    ChargingSlot.objects.create(charging_schedule=charging_schedule,
                                start_datetime=datetime.strptime(schedule_start, '%H:%M - %d/%m/%Y'),
                                end_datetime=datetime.strptime(schedule_end, '%H:%M - %d/%m/%Y'),
                                battery_level_gained=Decimal('0.1')
                                )

    url = reverse('override_charging_schedule', kwargs={'car_ae_id': car.ae_id})
    response = api_client.post(url)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['projected_battery_soc'] == expected_charge_level


def test_user_can_pause_schedule_and_see_new_battery_soc(api_client, car, charging_schedule, charging_slots):
    url = reverse('charging_schedule', kwargs={'car_ae_id': car.ae_id})
    response = api_client.get(url)


def test_user_sees_unchanged_battery_soc_when_car_not_at_home(api_client, car, charging_schedule, charging_slots):
    url = reverse('charging_schedule', kwargs={'car_ae_id': car.ae_id})
    response = api_client.get(url)

from datetime import datetime
from decimal import Decimal
from unittest import mock

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


@pytest.mark.parametrize('extra_charge_from_override,initial_battery_charge_level,expected_new_charge_level',
                         [(Decimal(0.1), Decimal(0.5), 0.7)])
def test_user_can_apply_charge_override_and_see_new_battery_soc(api_client, car, charging_schedule, charging_slot,
                                                                extra_charge_from_override,
                                                                initial_battery_charge_level,
                                                                expected_new_charge_level):
    car.battery_level = initial_battery_charge_level
    car.save()

    with mock.patch('CarChargingScheduler.services.battery_projection_calculator.calculate_override_component',
                    return_value=extra_charge_from_override):
        url = reverse('override_charging_schedule', kwargs={'car_ae_id': car.ae_id})
        response = api_client.post(url)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['projected_battery_soc'] == expected_new_charge_level


def test_user_can_pause_schedule_and_see_new_battery_soc(api_client, car, charging_schedule, charging_slot):
    """
    When a charging schedule is paused then no charging slots be utilized until the next day

    two scenarios

    all slots in same day - no extra capacity
    some slots today some slots tomorrow - some extra capacity but not all of it

    """

    # Scheduled is paused so no extra charge is added

    url = reverse('pause_charging_schedule', kwargs={'car_ae_id': car.ae_id})
    response = api_client.post(url)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['projected_battery_soc'] == car.battery_level

    # Schedule is unpaused so our extra charge capacity is added
    response = api_client.post(url)
    data = response.json()
    assert data['projected_battery_soc'] == 0.6


def test_user_sees_unchanged_battery_soc_when_car_not_at_home(api_client, car, charging_schedule, charging_slot):
    url = reverse('charging_schedule', kwargs={'car_ae_id': car.ae_id})
    response = api_client.get(url)

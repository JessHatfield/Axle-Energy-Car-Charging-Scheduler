from datetime import datetime
from decimal import Decimal
from unittest import mock

import pytest
from django.conf import settings
from django.urls import reverse
from rest_framework import status
from freezegun import freeze_time

from CarChargingScheduler.models import ChargingSlot

pytestmark = pytest.mark.django_db

"""
This file contains our acceptance tests

I've tried to split tests between this file and our services test file. This way I can test a bunch of extra edge 
cases without bloat

As a general pattern I try to keep business logic in service functions, this allows for easier re-use/testing

Edge cases relating to business logic (for example fractional slot calculations) stay in service function tests

Endpoint tests are then more about confirming that models/views/serializers/service functions work together across 
common scenarios

"""


@freeze_time('2024-01-01 01:00:00')
def test_user_can_retrieve_state_of_charge_and_charge_schedule(api_client, car, charging_schedule):
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

    assert data['charging_slots'] == [{'battery_level_gained': '0.10', 'end_datetime': '2024-01-01T02:00:00Z',
                                       'start_datetime': '2024-01-01T01:00:00Z'}]


@freeze_time('2024-01-01 01:00:00')
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


def test_user_override_stops_and_schedule_resumes_if_charging_stopped(api_client, car, charging_schedule):
    # Apply an override
    with mock.patch('CarChargingScheduler.services.battery_projection_calculator.calculate_override_component',
                    return_value=Decimal(0.1)):
        # Override applied so we get extra battery capacity
        url = reverse('override_charging_schedule', kwargs={'car_ae_id': car.ae_id})
        response = api_client.post(url)
        data = response.json()
        assert data['projected_battery_soc'] == 0.6
        assert data['is_override_applied'] is True

        # charging schedule has override applied
        charging_schedule.refresh_from_db()
        assert charging_schedule.override_applied_at is not None

        url = reverse('override_charging_schedule', kwargs={'car_ae_id': car.ae_id})
        response = api_client.post(url)
        data = response.json()
        assert data['projected_battery_soc'] == 0.5
        assert data['is_override_applied'] is False


@freeze_time('2024-01-01 01:00:00')
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
    assert data['is_schedule_paused'] == True

    # Schedule is unpaused so our extra charge capacity is added
    response = api_client.post(url)
    data = response.json()
    assert data['projected_battery_soc'] == 0.6
    assert data['is_schedule_paused'] == False


def test_paused_schedule_reactivates_the_following_day(api_client, car, charging_schedule,
                                                       charging_slots_spread_across_days):
    charging_slot_for_the_1st, charging_slot_for_the_2nd = charging_slots_spread_across_days

    with freeze_time('2024-01-01 01:00:00'):
        # Scheduled is paused so no extra charge is added
        url = reverse('pause_charging_schedule', kwargs={'car_ae_id': car.ae_id})
        response = api_client.post(url)
        data = response.json()
        assert data['projected_battery_soc'] == car.battery_level

    # Tomorrow comes around, the schedule should now be active again and our second slot should be applied
    with freeze_time('2024-01-02 01:00:00'):
        url = reverse('charging_schedule', kwargs={'car_ae_id': car.ae_id})
        response = api_client.get(url)
        data = response.json()
        assert Decimal(
            f'{data['projected_battery_soc']}') == car.battery_level + charging_slot_for_the_2nd.battery_level_gained


@freeze_time('2024-01-01 01:00:00')
def test_charge_scheduled_only_applied_when_car_is_at_home(api_client, car, charging_schedule, charging_slot):
    # Mark car as not at home
    url = reverse('car', kwargs={'car_ae_id': car.ae_id})
    response = api_client.put(url, data={'is_at_home': False})

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert False == data['is_at_home']

    # Retrieve Latest Charging Schedule
    url = reverse('charging_schedule', kwargs={'car_ae_id': car.ae_id})
    response = api_client.get(url)

    # Charge schedule has not been applied
    data = response.json()
    assert data['projected_battery_soc'] == 0.5
    assert data['is_schedule_paused'] == True

    # Mark car at home
    url = reverse('car', kwargs={'car_ae_id': car.ae_id})
    api_client.put(url, data={'is_at_home': True})

    #The charge schedule has now been applied
    url = reverse('charging_schedule', kwargs={'car_ae_id': car.ae_id})
    response = api_client.get(url)

    data = response.json()
    assert data['projected_battery_soc'] == 0.6
    assert data['is_schedule_paused'] == False


def test_override_cannot_be_applied_when_the_car_is_not_at_home(api_client, car, charging_schedule, charging_slot):
    assert charging_schedule.override_applied_at is None

    # Mark car as not at home
    url = reverse('car', kwargs={'car_ae_id': car.ae_id})
    api_client.put(url, data={'is_at_home': False})

    # Try to apply the override
    url = reverse('override_charging_schedule', kwargs={'car_ae_id': car.ae_id})
    response = api_client.post(url)
    data = response.json()

    #Check no override is applied
    assert data['is_override_applied'] is False
    assert data['projected_battery_soc'] == 0.5


def test_user_can_retrieve_cars(api_client, car):
    url = reverse('cars')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert data[0]['is_at_home'] == car.is_at_home
    assert Decimal(f'{data[0]['battery_level']}') == car.battery_level
    assert data[0]['ae_id'] == str(car.ae_id)

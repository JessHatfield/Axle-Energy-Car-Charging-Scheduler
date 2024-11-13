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
    assert data['projected_battery_soc'] == '0.7'


def test_user_can_apply_charge_override_and_see_new_battery_soc(api_client, car, charging_schedule, charging_slots):
    url = reverse('charging_schedule', kwargs={'ae_id': car.ae_id})

    response = api_client.get(url)


def test_user_can_pause_schedule_and_see_new_battery_soc(api_client, car, charging_schedule, charging_slots):
    url = reverse('charging_schedule', kwargs={'ae_id': car.ae_id})
    response = api_client.get(url)


def test_user_sees_unchanged_battery_soc_when_car_not_at_home(api_client, car, charging_schedule, charging_slots):
    url = reverse('charging_schedule', kwargs={'ae_id': car.ae_id})
    response = api_client.get(url)

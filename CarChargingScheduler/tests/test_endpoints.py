from datetime import datetime

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from CarChargingScheduler.models import User, Car, ChargingSlot, ChargingSchedule

pytestmark = pytest.mark.django_db


# Things we need to test


@pytest.fixture()
def user():
    return User.objects.create(username='TestUser')


@pytest.fixture()
def car(user):
    return Car.objects.create(user=user, )


@pytest.fixture()
def api_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture()
def charging_schedule(car):
    return ChargingSchedule.objects.create()


@pytest.fixture()
def charging_slots(charging_schedule):
    charging_slot_1 = ChargingSlot.objects.create(charging_schedule=charging_schedule,
                                                  start_time=datetime.strptime('01:00 - 01/01/2024',
                                                                               '%H:%M - %d/%m/%Y'),
                                                  end_time=datetime.strptime('02:00 - 01/01/2024', '%H:%M - %d/%m/%Y'))
    charging_slot_2 = ChargingSlot.objects.create(charging_schedule=charging_schedule,
                                                  start_time=datetime.strptime('05:00 - 01/01/2024',
                                                                               '%H:%M - %d/%m/%Y'),
                                                  end_time=datetime.strptime('07:00 - 01/01/2024', '%H:%M - %d/%m/%Y'))

    return charging_slot_1, charging_slot_2


def test_user_can_retrieve_state_of_charge(api_client, car, charging_schedule, charging_slots):
    url = reverse('charging_schedule')
    response = api_client.get(url)


def test_user_can_apply_charge_override_and_see_new_battery_soc(api_client, car, charging_schedule, charging_slots):
    url = reverse('charging_schedule')
    response = api_client.get(url)


def test_user_can_pause_schedule_and_see_new_battery_soc(api_client, car, charging_schedule, charging_slots):
    url = reverse('charging_schedule')
    response = api_client.get(url)


def test_user_sees_unchanged_battery_soc_when_car_not_at_home(api_client, car, charging_schedule, charging_slots):
    url = reverse('charging_schedule')
    response = api_client.get(url)

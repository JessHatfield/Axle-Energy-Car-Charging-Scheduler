import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


# Things we need to test


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

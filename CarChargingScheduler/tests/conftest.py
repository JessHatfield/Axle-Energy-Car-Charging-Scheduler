import pytest
from datetime import datetime
from rest_framework.test import APIClient
from CarChargingScheduler.models import User, Car, ChargingSlot, ChargingSchedule



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
    return ChargingSchedule.objects.create(car=car)


@pytest.fixture()
def charging_slots(charging_schedule):
    charging_slot_1 = ChargingSlot.objects.create(charging_schedule=charging_schedule,
                                                  start_datetime=datetime.strptime('01:00 - 01/01/2024',
                                                                               '%H:%M - %d/%m/%Y'),
                                                  end_datetime=datetime.strptime('02:00 - 01/01/2024', '%H:%M - %d/%m/%Y'))
    charging_slot_2 = ChargingSlot.objects.create(charging_schedule=charging_schedule,
                                                  start_datetime=datetime.strptime('05:00 - 01/01/2024',
                                                                               '%H:%M - %d/%m/%Y'),
                                                  end_datetime=datetime.strptime('07:00 - 01/01/2024', '%H:%M - %d/%m/%Y'))

    return charging_slot_1, charging_slot_2

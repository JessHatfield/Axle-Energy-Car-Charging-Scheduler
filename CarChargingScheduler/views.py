from django.utils import timezone
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from CarChargingScheduler.models import ChargingSlot, ChargingSchedule, Car
from CarChargingScheduler.serializers import ChargingScheduleSerializer, ChargingSlotSerializer, CarSerializer


class ChargingScheduleView(generics.RetrieveAPIView):
    serializer_class = ChargingScheduleSerializer

    def get_object(self):
        car_ae_id = self.kwargs['car_ae_id']
        return ChargingSchedule.objects.get(car=car_ae_id)

    def get(self, request, *args, **kwargs):
        data = self.retrieve(request, *args, **kwargs)
        return data


class PauseChargingScheduleView(generics.UpdateAPIView):
    queryset = ChargingSchedule.objects.all()
    serializer_class = ChargingScheduleSerializer

    def get_object(self):
        car_ae_id = self.kwargs['car_ae_id']
        return ChargingSchedule.objects.get(car=car_ae_id)

    def post(self, request, *args, **kwargs):

        charging_schedule = self.get_object()

        if charging_schedule.paused_until:
            charging_schedule.paused_until = None
        else:
            charging_schedule.paused_until = timezone.now()

        charging_schedule.save()

        return self.update(request, *args, **kwargs)


class OverrideChargingScheduleView(generics.UpdateAPIView):
    serializer_class = ChargingScheduleSerializer

    def get_object(self):
        car_ae_id = self.kwargs['car_ae_id']
        return ChargingSchedule.objects.get(car=car_ae_id)

    def post(self, request, *args, **kwargs):
        charging_schedule = self.get_object()

        # Toggle the override with each call
        if charging_schedule.override_applied_at:
            charging_schedule.override_applied_at = None
        elif charging_schedule.car.is_at_home and charging_schedule.override_applied_at is None:
            charging_schedule.override_applied_at = timezone.now()
        charging_schedule.save()

        return self.update(request, *args, **kwargs)


class ChargingSlotView(generics.ListAPIView):
    queryset = ChargingSlot.objects.all()
    serializer_class = ChargingSlotSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

class CarsView(generics.ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class CarView(generics.UpdateAPIView):
    serializer_class = CarSerializer

    def get_object(self):
        car_ae_id = self.kwargs['car_ae_id']
        return Car.objects.get(ae_id=car_ae_id)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

from django.utils import timezone
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from CarChargingScheduler.authentication import PreSharedKeyAuthentication

from CarChargingScheduler.models import ChargingSlot, ChargingSchedule, Car
from CarChargingScheduler.serializers import ChargingScheduleSerializer, ChargingSlotSerializer, CarSerializer


class ChargingScheduleView(generics.RetrieveAPIView):
    serializer_class = ChargingScheduleSerializer
    permission_classes = [PreSharedKeyAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        car_ae_id = self.kwargs['car_ae_id']
        return ChargingSchedule.objects.get(car=car_ae_id)

    def get(self, request, *args, **kwargs):
        data = self.retrieve(request, *args, **kwargs)
        return data


class PauseChargingScheduleView(generics.UpdateAPIView):
    queryset = ChargingSchedule.objects.all()
    authentication_classes = [PreSharedKeyAuthentication]
    permission_classes = [IsAuthenticated]
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
    authentication_classes = [PreSharedKeyAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ChargingScheduleSerializer

    def get_object(self):
        car_ae_id = self.kwargs['car_ae_id']
        return ChargingSchedule.objects.get(car=car_ae_id)

    def post(self, request, *args, **kwargs):
        charging_schedule = self.get_object()

        # Toggle the override with each call
        if charging_schedule.override_applied_at:
            charging_schedule.override_applied_at = None
        else:
            charging_schedule.override_applied_at = timezone.now()
        charging_schedule.save()

        return self.update(request, *args, **kwargs)


class ChargingSlotView(generics.ListAPIView):
    queryset = ChargingSlot.objects.all()
    authentication_classes = [PreSharedKeyAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ChargingSlotSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class CarView(generics.UpdateAPIView):
    queryset = Car.objects.all()
    authentication_classes = [PreSharedKeyAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CarSerializer

    def get_object(self):
        car_ae_id = self.kwargs['car_ae_id']
        return Car.objects.get(ae_id=car_ae_id)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

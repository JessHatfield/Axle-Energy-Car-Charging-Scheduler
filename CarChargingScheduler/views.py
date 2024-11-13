from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from CarChargingScheduler.authentication import PreSharedKeyAuthentication

from CarChargingScheduler.models import ChargingSlot, ChargingSchedule, Car


class ChargingScheduleView(generics.RetrieveAPIView):
    queryset = ChargingSchedule.objects.all()
    permission_classes = [PreSharedKeyAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        pass


class PauseChargingScheduleView(generics.UpdateAPIView):
    queryset = ChargingSchedule.objects.all()
    authentication_classes = [PreSharedKeyAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self):
        pass


class OverrideChargingScheduleView(generics.UpdateAPIView):
    queryset = ChargingSchedule.objects.all()
    authentication_classes = [PreSharedKeyAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self):
        pass


class ChargingSlotView(generics.ListAPIView):
    queryset = ChargingSlot.objects.all()
    authentication_classes = [PreSharedKeyAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        pass


class CarView(generics.RetrieveAPIView):
    queryset = Car.objects.all()
    authentication_classes = [PreSharedKeyAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self):
        pass

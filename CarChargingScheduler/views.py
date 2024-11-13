from rest_framework import generics

from CarChargingScheduler.models import ChargingSlot, ChargingSchedule, Car


class ChargingScheduleView(generics.RetrieveAPIView):
    queryset = ChargingSchedule.objects.all()

    def get(self, request, *args, **kwargs):
        pass


class PauseChargingScheduleView(generics.UpdateAPIView):

    def post(self):
        pass


class OverrideChargingScheduleView(generics.UpdateAPIView):

    def post(self):
        pass


class ChargingSlotView(generics.ListAPIView):
    queryset = ChargingSlot.objects.all()

    def get(self, request, *args, **kwargs):
        pass


class CarView(generics.RetrieveAPIView):
    queryset = Car.objects.all()

    def put(self):
        pass

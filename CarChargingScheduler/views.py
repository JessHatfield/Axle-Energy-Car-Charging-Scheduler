from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from CarChargingScheduler.authentication import PreSharedKeyAuthentication

from CarChargingScheduler.models import ChargingSlot, ChargingSchedule, Car
from CarChargingScheduler.serializers import ChargingScheduleSerializer


class ChargingScheduleView(generics.RetrieveAPIView):
    queryset = ChargingSchedule.objects.all()
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

    def post(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class OverrideChargingScheduleView(generics.UpdateAPIView):
    queryset = ChargingSchedule.objects.all()
    authentication_classes = [PreSharedKeyAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class ChargingSlotView(generics.ListAPIView):
    queryset = ChargingSlot.objects.all()
    authentication_classes = [PreSharedKeyAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class CarView(generics.RetrieveAPIView):
    queryset = Car.objects.all()
    authentication_classes = [PreSharedKeyAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

from rest_framework import serializers

from CarChargingScheduler.models import Car, ChargingSlot, ChargingSchedule


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['is_at_home','battery_level']


class ChargingSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargingSlot
        fields = ['start_datetime', 'end_datetime']


class ChargingScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargingSchedule
        fields = ['paused_until']



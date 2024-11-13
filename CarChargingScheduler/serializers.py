from rest_framework import serializers

from CarChargingScheduler.models import Car, ChargingSlot, ChargingSchedule


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['is_at_home', 'battery_level']


class ChargingSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargingSlot
        fields = ['start_datetime', 'end_datetime']


class ChargingScheduleSerializer(serializers.ModelSerializer):
    projected_battery_soc = serializers.SerializerMethodField()

    class Meta:
        model = ChargingSchedule
        fields = ['paused_until', 'projected_battery_soc']

    def get_projected_battery_soc(self, obj):
        return obj.projected_battery_soc

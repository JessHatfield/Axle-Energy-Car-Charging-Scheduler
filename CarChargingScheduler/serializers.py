from rest_framework import serializers

from CarChargingScheduler.models import Car, ChargingSlot, ChargingSchedule


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['is_at_home', 'battery_level']


class ChargingSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargingSlot
        fields = ['start_datetime', 'end_datetime','battery_level_gained']


class ChargingScheduleSerializer(serializers.ModelSerializer):
    projected_battery_soc = serializers.SerializerMethodField()
    is_schedule_paused=serializers.SerializerMethodField()
    is_override_applied=serializers.SerializerMethodField()

    charging_slots = ChargingSlotSerializer(many=True,required=False)

    class Meta:
        model = ChargingSchedule
        fields = ['paused_until', 'projected_battery_soc', 'charging_slots','is_schedule_paused','is_override_applied']

    def get_projected_battery_soc(self, obj):
        return obj.projected_battery_soc

    def get_is_schedule_paused(self,obj):
        return obj.scheduled_paused

    def get_is_override_applied(self,obj):
        if obj.override_applied_at:
            return True

        return False


from rest_framework import serializers


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model=Car
        field
from rest_framework import serializers
from .models import CustomerPotential


class CustomerPotentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerPotential

        fields = ['customer_name', 'customer_address',
                  'customer_type', 'keyword', 'radius', 'place_id', 'latitude_origin', 'longitude_origin', 'latitude_destination', 'longitude_destination', 'phone_number', 'distance_driving']

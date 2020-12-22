from rest_framework import viewsets
from . import models
from . import serializers


class CustomerPotentialViewset(viewsets.ModelViewSet):
    queryset = models.CustomerPotential.objects.all()
    serializer_class = serializers.CustomerPotentialSerializer

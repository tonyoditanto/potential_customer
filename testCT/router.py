from customertarget.viewsets import CustomerPotentialViewset
from rest_framework import routers

router = routers.DefaultRouter()
router.register('customerpotential', CustomerPotentialViewset)

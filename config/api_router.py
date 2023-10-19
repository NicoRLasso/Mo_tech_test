from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from mo_tech.customers.views import CustomerViewSet
from mo_tech.loans.views import LoanViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register(r"customers", CustomerViewSet, basename="customers")
router.register(r"loans", LoanViewSet, basename="loans")

app_name = "api"
urlpatterns = router.urls

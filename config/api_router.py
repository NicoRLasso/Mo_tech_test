from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from mo_tech.customers.views import HomeViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("customers", HomeViewSet, basename="customers")

app_name = "api"
urlpatterns = router.urls

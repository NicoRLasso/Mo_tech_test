from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CustomersConfig(AppConfig):
    name = "mo_tech.customers"
    verbose_name = _("Customers")

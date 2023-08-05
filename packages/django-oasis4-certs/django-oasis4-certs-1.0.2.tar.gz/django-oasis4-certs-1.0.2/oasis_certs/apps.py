# -*- coding: utf-8 -*-

#  Developed by CQ Inversiones SAS. Copyright ©. 2019 - 2023. All rights reserved.
#  Desarrollado por CQ Inversiones SAS. Copyright ©. 2019 - 2023. Todos los derechos reservado

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         24/01/23 5:29 PM
# Project:      CFHL Transactional Backend
# Module Name:  apps
# Description:
# ****************************************************************
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.apps import AppConfig


class OasisCerts(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "oasis_certs"
    verbose_name = _("Oasis4 Certificates Generator")

    def ready(self):
        settings.OASIS_CERTS_SEND_SUBJECT = getattr(settings, "OASIS_CERTS_SEND_SUBJECT", _("Sending of Certificate"))
        settings.OASIS_CERTS_SEND_TEMPLATE = getattr(settings, "OASIS_CERTS_SEND_TEMPLATE", "send_certificate.html")

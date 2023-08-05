# -*- coding: utf-8 -*-

#  Developed by CQ Inversiones SAS. Copyright ©. 2019 - 2023. All rights reserved.
#  Desarrollado por CQ Inversiones SAS. Copyright ©. 2019 - 2023. Todos los derechos reservado

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         1/02/23 21:03
# Project:      CFHL Transactional Backend
# Module Name:  admin_views
# Description:
# ****************************************************************
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class CertificateAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "enabled")
    fieldsets = (
        (
            None,
            {
                "fields": ("name", "category", ("cycle_type", "customer_type"), ("closed", "issue_date", "signed"), "enabled")
            }
        ),
        (
            _("Template data"),
            {
                "fields": ("template", "body_text", "footer_text", "query_text")
            }
        )
    )

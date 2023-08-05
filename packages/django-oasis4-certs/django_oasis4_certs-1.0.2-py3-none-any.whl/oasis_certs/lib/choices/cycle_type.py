# -*- coding: utf-8 -*-

#  Developed by CQ Inversiones SAS. Copyright ©. 2019 - 2023. All rights reserved.
#  Desarrollado por CQ Inversiones SAS. Copyright ©. 2019 - 2023. Todos los derechos reservado

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         6/02/23 19:37
# Project:      CFHL Transactional Backend
# Module Name:  period_type
# Description:
# ****************************************************************
from django.utils.translation import gettext_lazy as _
from zibanu.django.db import models


class CycleType(models.TextChoices):
    ANNUAL = "A", _("Annual")
    BIANNUAL = "S", _("Biannual")
    QUARTERLY = "T", _("Quarterly")
    BIMONTHLY = "B", _("Bimonthly")
    MONTHLY = "M", _("Monthly")
    NONE = "N", _("None")

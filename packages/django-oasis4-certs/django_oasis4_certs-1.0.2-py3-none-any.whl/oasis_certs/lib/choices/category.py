# -*- coding: utf-8 -*-

#  Developed by CQ Inversiones SAS. Copyright ©. 2019 - 2023. All rights reserved.
#  Desarrollado por CQ Inversiones SAS. Copyright ©. 2019 - 2023. Todos los derechos reservado

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         7/02/23 13:51
# Project:      CFHL Transactional Backend
# Module Name:  categories
# Description:
# ****************************************************************
from django.utils.translation import gettext_lazy as _
from zibanu.django.db import models


class Category(models.IntegerChoices):
    TAXES = 0, _("Taxes")
    COMMERCIAL = 1, _("Commercial")
    PARTNERS = 2, _("Partners")
    ACCOUNT_STATEMENTS = 3, _("Account Statements")
    FARM = 4, _("Farms")






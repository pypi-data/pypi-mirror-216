# -*- coding: utf-8 -*-

#  Developed by CQ Inversiones SAS. Copyright ©. 2019 - 2023. All rights reserved.
#  Desarrollado por CQ Inversiones SAS. Copyright ©. 2019 - 2023. Todos los derechos reservado

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         7/02/23 19:09
# Project:      CFHL Transactional Backend
# Module Name:  define_able
# Description:
# ****************************************************************
from django.utils.translation import gettext_lazy as _
from django import template

register = template.Library()


@register.simple_tag
def define_able(val: int = None):
    able = _("ABLE") if val == 1 else _("NOT ABLE")
    return able

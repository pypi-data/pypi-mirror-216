# -*- coding: utf-8 -*-

#  Developed by CQ Inversiones SAS. Copyright ©. 2019 - 2023. All rights reserved.
#  Desarrollado por CQ Inversiones SAS. Copyright ©. 2019 - 2023. Todos los derechos reservado

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         2/02/23 6:22
# Project:      CFHL Transactional Backend
# Module Name:  certificate
# Description:
# ****************************************************************
from zibanu.django.db import models


class Certificate(models.Manager):
    def get_by_category(self, category: int, customer_type: int = 0):
        return self.filter(category__exact=category, customer_type__lte=customer_type)


# -*- coding: utf-8 -*-

#  Developed by CQ Inversiones SAS. Copyright ©. 2019 - 2023. All rights reserved.
#  Desarrollado por CQ Inversiones SAS. Copyright ©. 2019 - 2023. Todos los derechos reservado

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         7/02/23 14:32
# Project:      CFHL Transactional Backend
# Module Name:  certificate
# Description:
# ****************************************************************
from oasis_certs.models import Certificate
from zibanu.django.rest_framework import serializers


class CertificateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Certificate
        fields = ("name", "id", "cycle_type")


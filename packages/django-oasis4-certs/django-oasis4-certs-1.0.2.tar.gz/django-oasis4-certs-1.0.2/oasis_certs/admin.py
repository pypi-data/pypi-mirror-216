# -*- coding: utf-8 -*-

#  Developed by CQ Inversiones SAS. Copyright ©. 2019 - 2023. All rights reserved.
#  Desarrollado por CQ Inversiones SAS. Copyright ©. 2019 - 2023. Todos los derechos reservado

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         1/02/23 21:08
# Project:      CFHL Transactional Backend
# Module Name:  admin
# Description:
# ****************************************************************
from django.contrib import admin
from oasis_certs.admin_views import CertificateAdmin
from oasis_certs.models import Certificate

admin.site.register(Certificate, CertificateAdmin)


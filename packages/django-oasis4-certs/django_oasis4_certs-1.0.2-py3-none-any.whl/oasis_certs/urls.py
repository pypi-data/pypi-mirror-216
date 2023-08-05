# -*- coding: utf-8 -*-

#  Developed by CQ Inversiones SAS. Copyright ©. 2019 - 2023. All rights reserved.
#  Desarrollado por CQ Inversiones SAS. Copyright ©. 2019 - 2023. Todos los derechos reservado

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         26/01/23 9:41 PM
# Project:      CFHL Transactional Backend
# Module Name:  urls
# Description:
# ****************************************************************
from django.urls import path
from django.urls import include
from oasis_certs.api import services
from rest_framework.routers import DefaultRouter

routers = DefaultRouter()

urlpatterns = [
    path(r"", include(routers.get_urls())),
    path(r"document/generator/", services.OasisCertsServices.as_view({"post": "gen_document"})),
    path(r"document/get/", services.OasisCertsServices.as_view({"post": "get_document"})),
    path(r"document/list/", services.OasisCertsServices.as_view({"post": "list_documents"})),
    path(r"document/send/", services.OasisCertsServices.as_view({"post": "send_document"}))
]


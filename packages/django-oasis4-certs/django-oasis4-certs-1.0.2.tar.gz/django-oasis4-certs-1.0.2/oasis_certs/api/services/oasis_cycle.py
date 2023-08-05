# -*- coding: utf-8 -*-

#  Developed by CQ Inversiones SAS. Copyright ©. 2019 - 2023. All rights reserved.
#  Desarrollado por CQ Inversiones SAS. Copyright ©. 2019 - 2023. Todos los derechos reservado

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         7/02/23 3:59
# Project:      CFHL Transactional Backend
# Module Name:  oasis_cycle
# Description:
# ****************************************************************
from django.utils.translation import gettext_lazy as _
from oasis.models import Cycle
from oasis.lib.serializers import CycleSerializer
from oasis_certs.models import Certificate
from rest_framework import status
from rest_framework.response import Response
from zibanu.django.utils import ErrorMessages
from zibanu.django.rest_framework.exceptions import APIException
from zibanu.django.rest_framework.exceptions import ValidationError
from zibanu.django.rest_framework.viewsets import ModelViewSet


class CycleServices(ModelViewSet):
    """
    Class that contains all services to get cycle entity
    """
    model = Cycle
    serializer_class = CycleSerializer

    def list(self, request, *args, **kwargs) -> Response:
        try:
            if "key" in request.data:
                certificate = Certificate.objects.get_by_key(request.data.get("key")).get()
                qs = self.model.objects.get_by_type(cycle_type=certificate.cycle_type)
                serializer = self.get_serializer(instance=qs, many=True)
                data_return = serializer.data
                status_return = status.HTTP_200_OK if len(data_return) > 0 else status.HTTP_204_NO_CONTENT
            else:
                raise ValidationError(_("The 'key' parameter is required."))
        except Certificate.DoesNotExist as exc:
            raise APIException(msg=ErrorMessages.NOT_FOUND, error=_("Certificate key does not exist."),
                               http_status=status.HTTP_404_NOT_FOUND) from exc
        except ValidationError as exc:
            raise APIException(msg=ErrorMessages.DATA_REQUIRED, error=exc.detail[0],
                               http_status=exc.status_code) from exc
        except Exception as exc:
            raise APIException(msg=ErrorMessages.NOT_CONTROLLED, error=str(exc)) from exc
        else:
            return Response(status=status_return, data=data_return)

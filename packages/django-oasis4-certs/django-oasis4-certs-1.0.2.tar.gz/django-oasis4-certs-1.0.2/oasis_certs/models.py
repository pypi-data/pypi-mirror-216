# -*- coding: utf-8 -*-

#  Developed by CQ Inversiones SAS. Copyright ©. 2019 - 2023. All rights reserved.
#  Desarrollado por CQ Inversiones SAS. Copyright ©. 2019 - 2023. Todos los derechos reservado

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         1/02/23 15:53
# Project:      CFHL Transactional Backend
# Module Name:  models
# Description:
# ****************************************************************
import uuid
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from oasis.lib.choices import CustomerType
from oasis_certs.lib.choices import Category
from oasis_certs.lib.choices import CycleType
from oasis_certs.lib import managers
from zibanu.django.db import models
from zibanu.django.repository.models import Document


class Certificate(models.Model):
    """
    Class model to represent certificate definition entity at database
    """
    name = models.CharField(max_length=80, blank=False, null=False, verbose_name=_("Certificate name"),
                            help_text=_("Name that appears as the title of the certificate"))
    category = models.IntegerField(choices=Category.choices, default=Category.TAXES, blank=False, null=False,
                                   verbose_name=_("Category"), help_text=_("Document category"))
    body_text = models.TextField(blank=False, null=False, verbose_name=_("Certificate text"),
                                 help_text=_("Text that goes inside the body of the certificate"))
    issue_date = models.DateField(blank=True, null=True, verbose_name=_("Issue date"), help_text=_("Issue date"))
    customer_type = models.IntegerField(choices=CustomerType.choices, default=CustomerType.ANYTHING, blank=False,
                                        null=False, verbose_name=_("Customer type"),
                                        help_text=_("Minimal customer type required for this document."))
    query_text = models.TextField(blank=False, null=False, verbose_name=_("Query text"),
                                  help_text=_("Text used to execute the query"))
    template = models.CharField(max_length=150, blank=False, null=False, verbose_name=_("Template to use"),
                                help_text=_("Template used to generate the certificate"))
    enabled = models.BooleanField(default=True, blank=False, null=False, verbose_name=_("Enabled"),
                                  help_text=_("Enabled"))
    footer_text = models.TextField(blank=True, null=False, verbose_name=_("Footer text"),
                                   help_text=_("Text that is located in the footer of the certificate"))
    cycle_type = models.CharField(max_length=1, default=CycleType.ANNUAL, blank=False, null=False,
                                  choices=CycleType.choices, verbose_name=_("Period type"),
                                  help_text=_("Type of periodicity of document."))
    closed = models.BooleanField(default=True, blank=False, null=False, verbose_name=_("Closing required"),
                                 help_text=_("The period must be closed."))
    signed = models.BooleanField(default=False, blank=False, null=False, verbose_name=_("Sign required"),
                                 help_text=_("The document require to be signed"))

    # Default Manager
    objects = managers.Certificate()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Certificate")
        verbose_name_plural = _("Certificates")

class CertificateFile(models.DatedModel):
    certificate = models.ForeignKey(Certificate, on_delete=models.PROTECT, blank=False, null=False)
    document = models.ForeignKey(Document, on_delete=models.PROTECT, blank=False, null=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, blank=False, null=False)
    year = models.IntegerField(blank=False, null=True)
    period = models.IntegerField(blank=False, null=True)
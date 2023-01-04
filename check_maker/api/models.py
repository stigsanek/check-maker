import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

TYPE_OF_CHECK = [
    ('kitchen', _('Check for kitchen')),
    ('client', _('Check for client')),
]

STATUS_OF_CHECK = [
    ('new', _('New')),
    ('rendered', _('Rendered')),
    ('printed', _('Printed')),
]


class MerchantPoint(models.Model):
    """Merchant point model"""
    class Meta:
        verbose_name = _('merchant point')
        verbose_name_plural = _('merchant points')

    name = models.CharField(
        max_length=100,
        help_text=_('Name')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_('Creation date')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text=_('Updated date')
    )

    def __str__(self) -> str:
        return self.name


class Printer(models.Model):
    """Printer model"""
    class Meta:
        verbose_name = _('printer')
        verbose_name_plural = _('printers')

    name = models.CharField(
        max_length=100,
        help_text=_('Name')
    )
    api_key = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        help_text=_('API access key')
    )
    check_type = models.CharField(
        max_length=10,
        choices=TYPE_OF_CHECK,
        help_text=_('Type of check')
    )
    merchant_point = models.ForeignKey(
        to=MerchantPoint,
        on_delete=models.PROTECT,
        help_text=_('Merchant point')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_('Creation date')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text=_('Updated date')
    )

    def __str__(self) -> str:
        return self.name


class Check(models.Model):
    """Check model"""
    class Meta:
        verbose_name = _('check')
        verbose_name_plural = _('checks')

    printer = models.ForeignKey(
        to=Printer,
        on_delete=models.PROTECT,
        help_text=_('Printer')
    )
    check_type = models.CharField(
        max_length=10,
        choices=TYPE_OF_CHECK,
        help_text=_('Type of check')
    )
    order = models.JSONField(
        help_text=_('Order data')
    )
    status = models.CharField(
        max_length=10,
        default=STATUS_OF_CHECK[0][0],
        choices=STATUS_OF_CHECK,
        help_text=_('Status of check')
    )
    pdf_file = models.FileField(
        null=True,
        help_text=_('PDF file')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_('Creation date')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text=_('Updated date')
    )

from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets

from check_maker.api import models, serializers


class MerchantPointViewSet(viewsets.ModelViewSet):
    """
    Views set for MerchantPoint
    list: Returns merchant point list
    create: Create merchant point
    retrieve: Returns merchant point
    partial_update: Update merchant point
    delete: Delete merchant point
    """
    queryset = models.MerchantPoint.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.MerchantPointListSerializer

        return serializers.MerchantPointItemSerializer


class PrinterViewSet(viewsets.ModelViewSet):
    """
    Views set for Printer
    list: Returns printer list
    create: Create printer
    retrieve: Returns printer
    partial_update: Update printer
    delete: Delete printer
    """
    queryset = models.Printer.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.PrinterListSerializer

        return serializers.PrinterItemSerializer


class CheckViewSet(viewsets.ModelViewSet):
    """
    Views set for Check
    list: Returns check list
    create: Create check
    retrieve: Returns check
    delete: Delete check
    """
    queryset = models.Check.objects.all()
    http_method_names = ['get', 'post', 'delete']

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.CheckListSerializer

        return serializers.CheckItemSerializer

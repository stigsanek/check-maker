from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models.deletion import ProtectedError
from django.utils.translation import gettext_lazy as _
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from check_maker.api import models, serializers


class CustomModelViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    """Custom ModelViewSet"""

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)

        except ProtectedError as err:
            data = {
                'detail': _('Cannot delete object as it is being used'),
                'protected_objects': [
                    {'id': o.pk, 'name': str(o)} for o in err.protected_objects
                ]
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

    def perform_destroy(self, instance):
        instance.delete()


class MerchantPointViewSet(CustomModelViewSet):
    """
    Views set for MerchantPoint
    list: Returns merchant point list
    create: Create merchant point
    retrieve: Returns merchant point
    partial_update: Update merchant point
    delete: Delete merchant point
    """
    queryset = models.MerchantPoint.objects.order_by('pk')
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.MerchantPointListSerializer

        return serializers.MerchantPointItemSerializer


class PrinterViewSet(CustomModelViewSet):
    """
    Views set for Printer
    list: Returns printer list
    create: Create printer
    retrieve: Returns printer
    partial_update: Update printer
    delete: Delete printer
    """
    queryset = models.Printer.objects.order_by('pk')
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.PrinterListSerializer

        return serializers.PrinterItemSerializer


class CheckViewSet(CustomModelViewSet):
    """
    Views set for Check
    list: Returns check list
    create: Create check
    retrieve: Returns check
    partial_update: Update check
    delete: Delete check
    get_checks_for_print: Returns rendered check by printer api key
    """
    queryset = models.Check.objects.order_by('pk')
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.CheckListSerializer

        if self.action == 'partial_update':
            return serializers.CheckUpdateItemSerializer

        return serializers.CheckItemSerializer

    @action(
        methods=['get'],
        detail=False,
        url_path=r'for-print/(?P<api_key>[\w-]+)',
        url_name='for-print'
    )
    def get_checks_for_print(self, request, api_key):
        try:
            printer = models.Printer.objects.get(api_key=api_key)
        except (ObjectDoesNotExist, ValidationError):
            raise NotFound

        qs = models.Check.objects.filter(
            printer_id=printer.pk, status='rendered'
        ).order_by('pk')

        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

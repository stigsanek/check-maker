import uuid

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import NotFound

from check_maker.api import models


class MerchantPointItemSerializer(serializers.ModelSerializer):
    """Serializer for item MerchantPoint"""
    class Meta:
        model = models.MerchantPoint
        fields = (
            'id',
            'name',
            'created_at',
            'updated_at'
        )


class MerchantPointListSerializer(serializers.ModelSerializer):
    """Serializer for list MerchantPoint"""
    class Meta:
        model = models.MerchantPoint
        fields = (
            'id',
            'url',
            'name'
        )


class PrinterItemSerializer(serializers.ModelSerializer):
    """Serializer for item Printer"""
    class Meta:
        model = models.Printer
        fields = (
            'id',
            'name',
            'api_key',
            'check_type',
            'merchant_point',
            'created_at',
            'updated_at'
        )


class PrinterListSerializer(serializers.ModelSerializer):
    """Serializer for list Printer"""
    class Meta:
        model = models.Printer
        fields = (
            'id',
            'url',
            'name',
            'check_type',
            'merchant_point'
        )


class CheckItemSerializer(serializers.ModelSerializer):
    """Serializer for item Check"""
    class Meta:
        model = models.Check
        fields = (
            'id',
            'printer',
            'check_type',
            'order',
            'status',
            'pdf_file',
            'created_at',
            'updated_at'
        )
        read_only_fields = (
            'id',
            'printer',
            'check_type',
            'status',
            'pdf_file',
            'created_at',
            'updated_at'
        )

    def validate_order(self, value):
        if not value.get('merchant_point'):
            raise serializers.ValidationError(
                _('The order must contain an ') + "'merchant_point'"
            )

        items = value.get('items')

        if not items or not isinstance(items, list):
            raise serializers.ValidationError(
                _('The order must contain a non-empty list of ') + "'items'"
            )

        for item in items:
            if not item.get('name') or not item.get('price'):
                raise serializers.ValidationError(
                    _('Each item must contain a ') + "'name', 'price'"
                )

        return value

    def create(self, validated_data):
        order = validated_data['order']
        printers = models.Printer.objects.filter(
            merchant_point=order['merchant_point']
        )

        if not printers:
            raise NotFound(_('No printers found for the merchant point'))

        instance = None
        order['uuid'] = str(uuid.uuid4())

        for printer in printers:
            validated_data['printer'] = printer
            validated_data['check_type'] = printer.check_type
            instance = super().create(validated_data)

        return instance


class CheckListSerializer(serializers.ModelSerializer):
    """Serializer for list Check"""
    class Meta:
        model = models.Check
        fields = (
            'id',
            'printer',
            'check_type',
            'status',
            'pdf_file'
        )

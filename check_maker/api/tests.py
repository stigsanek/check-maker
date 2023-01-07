from unittest.mock import patch

from celery.exceptions import Retry
from pytest import raises
from requests import RequestException
from rest_framework.reverse import reverse_lazy
from rest_framework.test import APITestCase

from check_maker.api.models import Check, MerchantPoint, Printer
from check_maker.api.tasks import create_checks


class TestAPI(APITestCase):
    """Base test class"""
    fixtures = ['data.json']


class TestMerchantPoints(TestAPI):
    """Tests for merchant points"""

    def setUp(self):
        self.mp = MerchantPoint.objects.get(pk=1)

    def test_list(self):
        url = reverse_lazy('merchantpoint-list')
        resp = self.client.get(url)
        data = resp.json()['results']

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['name'], self.mp.name)

    def test_create(self):
        url = reverse_lazy('merchantpoint-list')

        resp = self.client.post(path=url, data={})
        self.assertEqual(resp.status_code, 400)

        resp = self.client.post(path=url, data={'name': 'test'})
        self.assertEqual(resp.status_code, 201)
        self.assertTrue(
            MerchantPoint.objects.filter(name='test').exists()
        )

    def test_retrieve(self):
        url = reverse_lazy('merchantpoint-detail', args=[self.mp.pk])
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['name'], self.mp.name)

    def test_update(self):
        url = reverse_lazy('merchantpoint-detail', args=[self.mp.pk])
        data = {'name': ''}

        resp = self.client.put(path=url, data=data)
        self.assertEqual(resp.status_code, 405)

        resp = self.client.patch(path=url, data=data)
        self.assertEqual(resp.status_code, 400)

        data['name'] = 'test'

        resp = self.client.patch(path=url, data=data)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(
            MerchantPoint.objects.filter(name='test').exists()
        )

    def test_delete(self):
        mp_second_id = 2
        url_first = reverse_lazy('merchantpoint-detail', args=[self.mp.pk])
        url_second = reverse_lazy('merchantpoint-detail', args=[mp_second_id])

        resp = self.client.delete(url_first)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(len(resp.json()['protected_objects']), 3)
        self.assertTrue(
            MerchantPoint.objects.filter(pk=self.mp.pk).exists()
        )

        resp = self.client.delete(url_second)
        self.assertEqual(resp.status_code, 204)
        self.assertFalse(
            MerchantPoint.objects.filter(pk=mp_second_id).exists()
        )


class TestPrinters(TestAPI):
    """Tests for printers"""

    def setUp(self):
        self.printer = Printer.objects.get(pk=1)

    def test_list(self):
        url = reverse_lazy('printer-list')
        resp = self.client.get(url)
        data = resp.json()['results']

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(data), 3)
        self.assertEqual(data[0]['name'], self.printer.name)

        resp = self.client.get(f'{url}?check_type=test')
        self.assertEqual(resp.status_code, 400)

        resp = self.client.get(f'{url}?check_type=kitchen')
        data = resp.json()['results']
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(data), 1)

    def test_create(self):
        url = reverse_lazy('printer-list')
        data = {'name': 'test', 'check_type': 'test', 'merchant_point': 2}

        resp = self.client.post(path=url, data=data)
        self.assertEqual(resp.status_code, 400)

        data['check_type'] = 'kitchen'
        resp = self.client.post(path=url, data=data)
        api_key = resp.json()['api_key']

        self.assertEqual(resp.status_code, 201)
        self.assertTrue(api_key and len(api_key) > 16)
        self.assertTrue(
            Printer.objects.filter(name='test').exists()
        )

    def test_retrieve(self):
        url = reverse_lazy('printer-detail', args=[self.printer.pk])
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['name'], self.printer.name)

        resp = self.client.get(f'{url}?check_type=client')
        self.assertEqual(resp.status_code, 404)

    def test_update(self):
        url = reverse_lazy('printer-detail', args=[self.printer.pk])
        data = {'check_type': 'test'}

        resp = self.client.put(path=url, data=data)
        self.assertEqual(resp.status_code, 405)

        resp = self.client.patch(path=url, data=data)
        self.assertEqual(resp.status_code, 400)

        data['check_type'] = 'client'

        resp = self.client.patch(path=url, data=data)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(
            Printer.objects.filter(
                pk=self.printer.pk, check_type='client'
            ).exists()
        )

    def test_delete(self):
        printer_second_id = 3
        url_first = reverse_lazy('printer-detail', args=[self.printer.pk])
        url_second = reverse_lazy('printer-detail', args=[printer_second_id])

        resp = self.client.delete(url_first)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(len(resp.json()['protected_objects']), 2)
        self.assertTrue(
            Printer.objects.filter(pk=self.printer.pk).exists()
        )

        resp = self.client.delete(url_second)
        self.assertEqual(resp.status_code, 204)
        self.assertFalse(
            Printer.objects.filter(pk=printer_second_id).exists()
        )


class TestChecks(TestAPI):
    """Tests for checks"""

    def setUp(self):
        self.check = Check.objects.get(pk=1)

    def test_list(self):
        url = reverse_lazy('check-list')
        resp = self.client.get(url)
        data = resp.json()['results']

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(data), 4)
        self.assertEqual(data[0]['id'], self.check.pk)

        resp = self.client.get(f'{url}?check_type=test')
        self.assertEqual(resp.status_code, 400)

        resp = self.client.get(f'{url}?check_type=kitchen')
        data = resp.json()['results']
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(data), 2)

    @patch('check_maker.api.tasks.create_checks.delay')
    def test_create(self, mock_delay):
        url = reverse_lazy('check-list')
        data = {'order': {'merchant_point': 2, 'total_price': 20}}

        resp = self.client.post(path=url, data=data, format='json')
        self.assertEqual(resp.status_code, 400)

        data['order']['items'] = [{'name': 'test', 'price': 10, 'count': 2}]
        resp = self.client.post(path=url, data=data, format='json')

        self.assertEqual(resp.status_code, 400)
        self.assertTrue('No printers found' in resp.json()['order'][0])

        data['order']['merchant_point'] = 1
        resp = self.client.post(path=url, data=data, format='json')
        order_uuid = resp.json()['uuid']
        checks_len = len(Check.objects.filter(order__uuid=order_uuid))

        self.assertEqual(resp.status_code, 201)
        self.assertTrue(order_uuid and len(order_uuid) > 16)
        self.assertEqual(checks_len, 3)

    def test_retrieve(self):
        url = reverse_lazy('check-detail', args=[self.check.pk])
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['id'], self.check.pk)

        resp = self.client.get(f'{url}?status=printed')
        self.assertEqual(resp.status_code, 404)

    def test_update(self):
        url = reverse_lazy('check-detail', args=[self.check.pk])
        data = {'status': 'test'}

        resp = self.client.put(path=url, data=data)
        self.assertEqual(resp.status_code, 405)

        resp = self.client.patch(path=url, data=data)
        self.assertEqual(resp.status_code, 400)

        data['status'] = 'printed'

        resp = self.client.patch(path=url, data=data)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(
            Check.objects.filter(pk=self.check.pk, status='printed').exists()
        )

    def test_delete(self):
        url = reverse_lazy('check-detail', args=[self.check.pk])
        resp = self.client.delete(url)

        self.assertEqual(resp.status_code, 204)
        self.assertFalse(
            Check.objects.filter(pk=self.check.pk).exists()
        )

    def test_get_checks_for_print(self):
        self.check.status = 'rendered'
        self.check.save()

        api_key = Printer.objects.get(pk=1).api_key
        url_first = reverse_lazy('check-for-print', args=[api_key])
        url_second = reverse_lazy('check-for-print', args=['test'])

        resp = self.client.get(url_first)
        data = resp.json()['results']

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['id'], self.check.pk)

        resp = self.client.get(url_second)
        self.assertEqual(resp.status_code, 404)

    @patch('check_maker.api.tasks.convert_html_to_pdf')
    @patch('check_maker.api.tasks.create_checks.retry')
    def test_create_check(self, mock_retry, mock_convert_html_to_pdf):
        create_checks(self.check.order['uuid'])
        check = Check.objects.get(pk=1)

        self.assertEqual(check.status, 'rendered')
        self.assertTrue(check.order['uuid'] in check.pdf_file.name)

        mock_retry.side_effect = Retry()
        mock_convert_html_to_pdf.side_effect = RequestException()
        with raises(Retry):
            create_checks(check.order['uuid'])

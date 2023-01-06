import uuid
from pathlib import Path
from tempfile import mkdtemp

from django.conf import settings
from django.test import TestCase
from django.urls import reverse_lazy


class TestTasks(TestCase):
    """Tests for download"""

    def setUp(self):
        self.tmp_dir = Path(mkdtemp())
        settings.MEDIA_ROOT = self.tmp_dir

    def test_download(self):
        tmp_file = self.tmp_dir / 'test.txt'
        expected = str(uuid.uuid4())

        with open(file=tmp_file, mode='w') as f:
            f.write(expected)

        url_first = reverse_lazy('media', args=['test.txt'])
        url_second = reverse_lazy('media', args=['test2.txt'])

        resp = self.client.get(url_first)
        got = resp.getvalue().decode('utf-8')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(got, expected)

        resp = self.client.get(url_second)
        self.assertEqual(resp.status_code, 404)

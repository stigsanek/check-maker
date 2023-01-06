from django.conf import settings
from django.http import FileResponse, Http404


def download(request, path):
    file_path = settings.MEDIA_ROOT / path

    if not file_path.exists():
        raise Http404

    response = FileResponse(open(file_path, 'rb'))
    response['Content-Disposition'] = f'inline; filename={file_path.name}'
    return response

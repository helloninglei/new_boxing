# coding=utf-8
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from boxing_app.forms import UploadFileForm
from boxing_app.services import file_service


@require_POST
def upload_file(request):
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
        f = request.FILES['file']
        url = file_service.save_upload_file(f)
        return JsonResponse({"url": url})
    return JsonResponse({'data': form.errors})

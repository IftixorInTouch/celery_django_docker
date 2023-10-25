from django.http import HttpResponse
from . import tasks


def home(request):
    tasks.download_cat.delay()
    return HttpResponse("Cat is uploading")

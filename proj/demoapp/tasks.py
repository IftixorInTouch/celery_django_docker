import requests
import uuid
from celery import shared_task
from django.conf import settings

CAT_URL = "https://cataas.com/cat"


@shared_task
def download_cat():
    response = requests.get(url=CAT_URL)
    file_extension = response.headers.get('Content-Type').split('/')[1]
    file_name = (settings.BASE_DIR / 'media' / 'cats' / (str(uuid.uuid4()))).with_suffix(f'.{file_extension}')
    with open(file_name, 'wb') as file:
        for chunk in response.iter_content(chunk_size=128):
            file.write(chunk)
    return True

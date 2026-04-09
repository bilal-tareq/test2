import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'supercareer.settings')
django.setup()

from django.test import Client

c = Client()
try:
    response = c.post('/api/forgot-password/', json.dumps({'email': 'test@example.com'}), content_type='application/json')
    print("Status Code:", response.status_code)
    try:
        print("Response JSON:", response.json())
    except Exception:
        print("Response Content:", response.content)
except Exception as e:
    import traceback
    traceback.print_exc()

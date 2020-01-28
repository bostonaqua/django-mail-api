from django.http import HttpResponseServerError
from django.shortcuts import HttpResponse
import json


def index(request):
    return HttpResponse("*\-(^_^)-/*")


def save_events_json(request):
    if request.is_ajax():
        if request.method == 'POST':
            json_data = json.loads(request.body)
            try:
                host = json_data['host']
                port = json_data['port']
                mail_from = json_data['from']
                mail_to = json_data['to']
                subject = json_data['subject']
                message = json_data['message']
            except KeyError:
                HttpResponseServerError("Malformed data!")
    return HttpResponse("OK")

from django.http import HttpResponseServerError
from django.core.mail import send_mail
from django.core.mail.backends.smtp import EmailBackend
from django.shortcuts import HttpResponse
import json

from django.views.decorators.csrf import csrf_exempt


def index(request):
    return HttpResponse("*\-(^_^)-/*")


@csrf_exempt
def send_mail_view(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        try:
            host = json_data['host']
            port = json_data['port']
            mail_from = json_data['from']
            mail_to = json_data['to']
            subject = json_data['subject']
            message = json_data['message']
            username = json_data['username']
            password = json_data['password']
            send_mail(
                "{} - {}".format(subject, mail_from),
                "{}\n\n---\nFrom: {}".format(message, mail_from),
                "{}".format(username),
                ['{}'.format(mail_to)],
                auth_user=username,
                auth_password=password,
                connection=EmailBackend(host=host, port=port, username=username, password=password)
            )
        except KeyError:
            return HttpResponseServerError("Malformed data!")
        return HttpResponse("OK")
    else:
        return HttpResponseServerError("Service unavailable")

from django.http import HttpResponseServerError, JsonResponse
from django.core.mail import send_mail
from django.core.mail.backends.smtp import EmailBackend
from django.shortcuts import HttpResponse
import json

from django.views.decorators.csrf import csrf_exempt


def index(request):
    return HttpResponse("*\-(^_^)-/*")


@csrf_exempt
def send_mail_view(request):
    if request.method == 'OPTIONS':
        response = HttpResponse("ok")
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Headers"] = "User-Agent,Cache-Control,Content-Type"
        response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response["Access-Control-Expose-Headers"] = "Content-Length,Content-Range"
        return response
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
            send_mail(
                "{} - {}".format(subject, mail_from),
                "{}\n\n---\nFrom: {}".format(message, mail_from),
                "{}".format(username),
                ['{}'.format(mail_to)],
                connection=EmailBackend(host=host, port=port, username=username, password="***", use_tls=True)
            )
            response = JsonResponse(
                {"status": "completed"}
            )
            response["Access-Control-Allow-Origin"] = "*"
            response["Access-Control-Allow-Headers"] = "User-Agent,Cache-Control,Content-Type"
            response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
            response["Access-Control-Expose-Headers"] = "Content-Length,Content-Range"
        except (KeyError, ConnectionRefusedError) as e:
            err_response = HttpResponseServerError("Malformed data! {}".format(e))
            err_response["Access-Control-Allow-Origin"] = "*"
            err_response["Access-Control-Allow-Headers"] = "User-Agent,Cache-Control,Content-Type"
            err_response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
            err_response["Access-Control-Expose-Headers"] = "Content-Length,Content-Range"
            return err_response
        return response
    else:
        return HttpResponseServerError("Service unavailable")

from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('sendmail', views.send_mail_view, name='send-mail'),
]

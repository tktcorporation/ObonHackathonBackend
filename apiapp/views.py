import json

from apiapp.models import Message
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# from django.shortcuts import render
from django.views.generic import View


class TestApiView(View):
    def get(self, request):
        return JsonResponse({"status": "ok"})


@method_decorator(csrf_exempt, name="dispatch")
class MessagesApiView(View):
    def get(self, request):
        return JsonResponse(
            {
                "messages": [
                    {"message": message.value} for message in Message.objects.all()
                ]
            }
        )

    def post(self, request):
        body_unicode = request.body.decode("utf-8")
        body = json.loads(body_unicode)
        value = body["message"]
        Message.objects.create(value=value)
        return HttpResponse("OK")

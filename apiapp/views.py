import json
import random

from apiapp.models import Message
from django.core import serializers
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# from django.shortcuts import render
from django.views.generic import View


class TestApiView(View):
    def get(self, request):
        return JsonResponse({"status": "ok"})


@method_decorator(csrf_exempt, name="dispatch")
class MessagesApiView(View):
    def get(self, request) -> JsonResponse:
        # TODO 5min 以内のものだけ取りたい
        messages = [m for m in Message.objects.all()]

        # 件数が5以上の場合は5件まで絞る
        if len(messages) > 5:
            messages_sample = random.sample(messages, 5)
        else:
            messages_sample = messages

        print(request.GET.get("datetime"))

        if "datetime" in request.GET:
            bool = request.GET.get("datetime")
            if bool:
                return JsonResponse(
                    {
                        "messages": [
                            {
                                "message": message.value,
                                "datetime": message.created_at.strftime(
                                    "%Y-%m-%dT%H:%M:%S%z"
                                ),
                            }
                            for message in messages_sample
                        ]
                    }
                )

        return JsonResponse(
            {"messages": [{"message": message.value} for message in messages_sample]}
        )

    def post(self, request):
        body_unicode = request.body.decode("utf-8")
        body = json.loads(body_unicode)
        value = body["message"]
        max_length = 10
        if len(value) > max_length:
            return HttpResponseBadRequest(f"文字数制限: {max_length}")
        Message.objects.create(value=value)
        return HttpResponse("OK", status=201)

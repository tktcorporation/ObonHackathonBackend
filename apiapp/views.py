import json
import random
from datetime import datetime

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
        timestamp_from_filter = None
        if "timestamp_from" in request.GET:
            timestamp_from = request.GET.get("timestamp_from")
            try:
                timestamp_from_filter = datetime.fromtimestamp(int(timestamp_from))
            except Exception as e:
                print(e)

        if timestamp_from_filter:
            messages = [
                m for m in Message.objects.filter(updated_at__gt=timestamp_from_filter)
            ]
        else:
            messages = [m for m in Message.objects.all()]

        # 件数が5以上の場合は5件まで絞る
        # if len(messages) > 5:
        #     messages_sample = random.sample(messages, 5)
        # else:
        #     messages_sample = messages

        messages_sample = messages
        random.shuffle(messages_sample)

        return JsonResponse(
            {
                "messages": [
                    {
                        "message": message.value,
                        "timestamp": message.created_at.timestamp(),
                    }
                    for message in messages_sample
                ]
            }
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

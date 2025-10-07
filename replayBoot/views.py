from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import ProductSerializer
from rest_framework import status
from .models import Product
from django.conf import settings
import requests

verify_token = settings.VERIFY_TOKEN


class productList(APIView):

    def get_queryset(self):
        return Product.objects.all()

    # ✅ تأكيد الاشتراك من فيسبوك (التحقق من الـ verify token)
    def get(self, request):
        mode = request.GET.get("hub.mode")
        token = request.GET.get("hub.verify_token")
        challenge = request.GET.get("hub.challenge")

        if mode == "subscribe" and token == verify_token:
            print("✅ Webhook verified successfully.")
            return HttpResponse(challenge, status=200)
        else:
            print("❌ Token verification failed.")
            return HttpResponse("Token Error", status=403)

    # ✅ إرسال رسالة من البوت
    def send_message(self, sender_id, text):
        url = "https://graph.facebook.com/v23.0/me/messages"
        params = {"access_token": settings.PAGE_ACCESS_TOKEN}
        data = {
            "recipient": {"id": sender_id},
            "message": {"text": text}
        }
        response = requests.post(url, params=params, json=data)
        print("📤 Message sent:", response.text)

    def post(self, request):
        data = request.data
        print('#data#',data) 

        if "entry" in data:
            for entry in data["entry"]:
                if "messaging" in entry:
                    for event in entry["messaging"]:
                        sender_id = event["sender"]["id"]  # PSID
                        if "message" in event:
                            message_text = event["message"].get("text", "")
                            print(f"💬 New message from {sender_id}: {message_text}")
                            self.send_message(sender_id, "مرحبًا 👋! تم استلام رسالتك.")
                if "changes" in entry:
                    for change in entry["changes"]:
                        value = change.get("value", {})
                        if value.get("item") == "comment":  # تحقق أن الحدث تعليق
                            comment_text = value.get("message", "")
                            commenter = value.get("from", {})
                            commenter_id = commenter.get("id")
                            commenter_name = commenter.get("name")

                            print(f"🗨️ New comment from {commenter_name}: {comment_text}")

                            if commenter_id:
                                reply_text = f"مرحبًا {commenter_name}! 👋 شكراً لتعليقك: {comment_text}"
                                self.send_message(commenter_id, reply_text)

        return HttpResponse("EVENT_RECEIVED", status=200)

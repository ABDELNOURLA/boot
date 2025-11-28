from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import ProductSerializer
from rest_framework import status
from .models import Product
from django.conf import settings
import requests
import json

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

    def reply_to_comment(self, comment_id, text):
        """رد على التعليق نفسه على المنشور"""
        url = f"https://graph.facebook.com/v17.0/{comment_id}/comments"
        payload = {"message": text}
        params = {"access_token": self.PAGE_ACCESS_TOKEN}
        response = requests.post(url, data=payload, params=params)
        print("Reply status:", response.status_code, response.text)

    def post(self, request):
        data = json.loads(request.body)  # استخدام json.loads إذا لم تستخدم DRF
        print('#data#', data)

        if "entry" in data:
            for entry in data["entry"]:
                if "changes" in entry:
                    for change in entry["changes"]:
                        value = change.get("value", {})
                        # تحقق أن الحدث تعليق
                        if value.get("item") == "comment":
                            comment_text = value.get("message", "")
                            # التحقق من معرف التعليق سواء كان 'id' أو 'comment_id'
                            comment_id = value.get("comment_id") or value.get("id")
                            commenter = value.get("from", {})
                            commenter_name = commenter.get("name", "مستخدم")

                            print(f"🗨️ New comment from {commenter_name}: {comment_text}")

                            if comment_id:
                                reply_text = " يرجئ الاعجاب بصفحتنا لنستطيع الرد علئ اسئلتك او الاتصال علئ الرقم :0658984615"
                                self.reply_to_comment(comment_id, reply_text)

        return HttpResponse("EVENT_RECEIVED", status=200)

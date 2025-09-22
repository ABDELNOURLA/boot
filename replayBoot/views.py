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
    
    
def get(self, request):
    mode = request.GET.get("hub.mode")
    token = request.GET.get("hub.verify_token")
    challenge = request.GET.get("hub.challenge")

    if mode == "subscribe" and token == verify_token:
        return HttpResponse(challenge, status=200)  # نص عادي، مش JSON
    return HttpResponse("Token Error", status=403)

    

    def send_message(self, sender_id, text):
        url = "https://graph.facebook.com/v19.0/me/messages"
        params = {"access_token": settings.PAGE_ACCESS_TOKEN}
        data = {
            "recipient": {"id": sender_id},
            "message": {"text": text}
        }
        requests.post(url, params=params, json=data)
    #def post(self,request):
        #data=request.data
        
       # if "entry" in data:
       #    for entry in data["entry"]:
        #        if "messaging" in entry:
         #           for event in entry["messaging"]:
          #              sender_id = event["sender"]["id"]  # PSID
           #             if "message" in event:
                            # text = event["message"].get("text", "")
      #  text = text[9:]
      #  self.send_message(sender_id,"hello")

        #if Product.objects.get(name=text):
        #    response_text = f"{Product.objects.get("price")} هى{text}سعر المنتج"
         #   self.send_message(sender_id,response_text)

def post(self, request):
    data = request.data

    if "entry" in data:
        for entry in data["entry"]:
            if "messaging" in entry:
                for event in entry["messaging"]:
                    sender_id = event["sender"]["id"]  # PSID
                    if "message" in event:
                        # أي رسالة تجيك → رد بـ "hello"
                        self.send_message(sender_id, "hello")

    return HttpResponse("EVENT_RECEIVED", status=200)


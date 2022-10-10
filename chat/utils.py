import json
import logging

import requests
from django.http import HttpResponse



def send_notification(registration_ids, message_title):
    fcm_api = "AAAAHYUDj9Q:APA91bHhlGGO6NJThoqobAIvCgovHVDIwKFvGO1yzoCz1I-4_cbkTKg6PZ5iEpU_xBn-fNIwUb6vuAkH6RvmlnwrCXeZ0zQhuBhDQgRSgUxgTPW56qzi6ShF4PmW4voOUIe07zbpytSv"
    url = "https://fcm.googleapis.com/fcm/send"

    headers = {
        "Content-Type": "application/json",
        "Authorization": 'key=' + fcm_api}

    payload = {
        "registration_ids": registration_ids,
        "priority": "high",
        "data": {
            "token": registration_ids[0],

        },
        "notification": {
            "body": message_title,
            "title": 'لاوینو',
            "image": "https://i.ytimg.com/vi/m5WUPHRgdOA/hqdefault.jpg?sqp=-oaymwEXCOADEI4CSFryq4qpAwkIARUAAIhCGAE=&rs=AOn4CLDwz-yjKEdwxvKjwMANGk5BedCOXQ",
            "icon": "https://yt3.ggpht.com/ytc/AKedOLSMvoy4DeAVkMSAuiuaBdIGKC7a5Ib75bKzKO3jHg=s900-c-k-c0x00ffffff-no-rj",

        }
    }

    result = requests.post(url, data=json.dumps(payload), headers=headers)
    print(result.json())

import requests


def send_otp(phone_number, code):
    requests.get(
        f"http://ws3584.isms.ir/sendWS?username=7bluesky&password=@7BS123456&mobiles[]={phone_number}&body= کد شما برای عضویت در برنامه{code}"
    )

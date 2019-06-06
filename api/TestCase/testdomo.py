import hmac
import hashlib

appkey = "JH584b9e36405a5e6201dd2649e9340b63"
APP_SECRET = "f7552811e14e70d18726005b5375cf35"
signature = hmac.new(bytes(appkey, encoding='utf-8'), bytes(APP_SECRET, encoding='utf-8'),
                     digestmod=hashlib.sha256).digest()

HEX = signature.hex()
print(HEX)

import requests
import hashlib
import hmac
url='http://app-portal-qd.yingyinglicai.org/app/gateway.do'
rds="""{
  "osVersion" : "12.2",
  "clientIp" : "10.20.2.131",
  "mobileType" : "iPhone 6",
  "clientCity" : "杭州市",
  "deviceId" : "94154df5932eecf2cbfe9cc17bfe27f0",
  "clientProvince" : "浙江省",
  "appSourceId" : "1",
  "deviceName" : "iPhone",
  "wifiMac" : "",
  "carrierOperator" : "中国电信",
  "appVersion" : "1.2.7",
  "lng" : "120.161706",
  "clientRegion" : "中国浙江省杭州市下城区绍兴路390号",
  "pushId" : "EwX4E5NrMFWkOFp+\/3SYZo\/JU2yJHQhvWlVTPUeN3Tzu1oORgOT9Vr5Q39w8wTIR",
  "screenHeight" : "667",
  "resolution" : "750*1334",
  "userType" : "1",
  "loginType" : "1",
  "mac" : "02:00:00:00:00:00",
  "appName" : "YYYQ",
  "token" : "0ca44d82ff060aed076bd9bc6b9a0b7c656b4fed",
  "networkStatus" : "Wifi",
  "mobile" : "15305810688",
  "screenWidth" : "375",
  "lat" : "30.303235",
  "tId" : "eyJ0b2tlbklkIjoieGRBaElPcFRndGRGQjd5NXZEWUFUSWw0VXpBNUs4YlI2dVwvSjJtSjVuUEtsd0N4V0Qrc3lvQW1QVHlpTGlTVFhXYWxaOVcwOGx3a1lnYVdSMFBCRGp3PT0iLCJvcyI6ImlPUyIsInByb2ZpbGVUaW1lIjo5OTksInZlcnNpb24iOiIzLjEuNyJ9",
  "passWord" : "1990926nba",
  "device" : "ios",
  "idfa" : "2BE24F31-3630-49B3-B0D0-B6EEF10AE913"
}"""
pagms={'at':'auth.login','fr':None,'rd':rds,'v':'1.0.0'}
req=requests.post(url,params=pagms,headers={'Content-Type':'application/json; charset=UTF-8'})
# urls='http://yyyq-app-bff-qd.yingyinglicai.org/api/api_collaboration/merchant_order/trial_calculation'
token=req.cookies['YYYQAUTHTOKEN']
# pagm={'orderNo':'lo331778851153903616','loanAmount':'3500','periodDuration':'WEEK','periodNum':1}
# reqs=requests.get(urls,params=pagm,cookies={'YYYQAUTHTOKEN':token})
# print(token)
urls = 'http://yhyyyqapi-portal.yingyingwork.info/open-api/loan-market/merchant/approve_status_notification'
pagms = {
  'APP_KEY':"JH584b9e36405a5e6201dd2649e9340b63",
  'APP_SECRET':"f7552811e14e70d18726005b5375cf35",
  "orderNo": "lo331141649944281088",
  "approvalStatus": 13000,
  "approvalTime": "2019-06-05 14:31:46",
  "approvalAmount": 300000,
  "term": 3,
  "termType": 5,
  "rate": 36,
  "rateType": 4,
  "remark": "审核结果test"
}
req1 = requests.post(urls,params=pagms,cookies={'YYYQAUTHTOKEN':token},headers={'Content-Type':'application/json'})
print(req1.text)

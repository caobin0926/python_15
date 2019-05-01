import requests
from api.comon import config
from api.comon import paths


class HttpRequest:
    def __init__(self):
        # 打开session
        self.session = requests.session()

    # http请求方法
    def request(self, method, url, parmas, json=None):
        conf=config.ReadConfig(paths.gloads_file)
        url = conf.get('api', 'url') + url
        if method.lower() == 'post':
            if json:
                resp = self.session.request(method, url, json=parmas)
            else:
                resp = self.session.request(method, url, data=parmas)
        elif method.lower() == 'get':
            resp = self.session.request(method, url, params=parmas)
        else:
            print('暂不支持其他方法')
        return resp

    def sessionclose(self):
        self.session.close()


if __name__ == '__main__':
    req = HttpRequest()
    resp1 = req.request('Post', '/member/login',
                        {'mobilephone': '18206573747', 'pwd': '123456'})
    resp2 = req.request('Post', '/member/bidLoan',
                        {'memberId': 278,
                         'password': '123456',
                         'loanId': 473,
                         'amount': 100})
    print(resp2.text)
    print(resp2.status_code)
    print(resp1.cookies)
    print(resp2.request._cookies)
    req.sessionclose()

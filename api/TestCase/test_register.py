from unittest import TestCase
from api.comon.httprequest import HttpRequest
from api.comon.do_excel import Excel
import json
import allure
import pytest
from api.comon.do_re import replace
from api.comon import paths
from api.comon.Mylogging import Logs


# 定义一个测试注册接口的类
@allure.feature('注册接口')
class TestRegister:
    ex = Excel(paths.cases_file, 'register')
    datas = ex.get_case()

    def setup_class(self):
        self.req_request = HttpRequest()  # 实例化HttpRequest对象
        self.logger = Logs('register')
        self.logger.getlogs('info', '------------开始执行测试用例------------')

    @allure.story('注册模块')
    @pytest.mark.parametrize('case', datas)
    def test_register(self, case):
        self.logger.getlogs('info', '测试场景：{}'.format(case.title))
        case.data = replace(case.data, paths.gloads_file, 'testdata')
        try:

            # print (case.data)
            self.logger.getlogs('debug', '请求参数：{}'.format(case.data))
            req_reqsond = self.req_request.request(case.method, case.url, eval(case.data))  # 发送请求
            case.actual = json.loads(req_reqsond.text)
            self.logger.getlogs('debug', '响应结果：{}'.format(case.actual))
            # print(req_reqsond.status_code)
            allure.attach('{}'.format(eval(case.expected)), '预期结果')
            allure.attach('{}'.format(case.actual), '实际结果')
            assert eval(case.expected) == case.actual  # 断言实际结果和预期结果
            case.result = 'PASS'
        except AssertionError as asser:
            case.result = 'FAIL'
            raise asser
            self.logger.getlogs('error', '断言失败原因：{}'.format(asser))
        finally:
            TestRegister.ex.set_write(case.case_id, req_reqsond.text, case.result)
            allure.attach('{}'.format(case.result), '断言结果')
            self.logger.getlogs('info', '测试结果：{}'.format(case.result))

    def teardown_class(self):
        self.req_request.sessionclose()
        self.logger.getlogs('info','------------测试完成------------')

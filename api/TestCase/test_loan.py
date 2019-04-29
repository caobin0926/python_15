from api.comon.httprequest import HttpRequest
from api.comon.do_excel import Excel
from api.comon import paths
import json
import pytest
import allure
from api.comon.Mylogging import Logs
from api.comon.do_re import replace
from api.comon.do_mysql import Mysql
from api.comon.do_re import TestData

"""
定义测试上标类
"""


@allure.feature('上标接口')
class TestLoan:
    ex = Excel(paths.cases_file, 'loan')
    datas = ex.get_case()

    def setup_class(self):
        self.request = HttpRequest()
        self.logger = Logs('loan')
        self.my_msql = Mysql()
        self.logger.getlogs('info', '------------开始执行测试用例------------')

    @allure.story('上标模块')
    @pytest.mark.parametrize('cases', datas)
    def test_loan(self, cases):
        self.logger.getlogs('info', '测试场景：{}'.format(cases.title))
        cases.data = replace(cases.data, paths.gloads_file, 'testdata')
        self.logger.getlogs('debug', '请求参数：{}'.format(cases.data))
        resp = self.request.request(cases.method, cases.url, eval(cases.data))
        cases.actual = json.loads(resp.text)
        if int(cases.case_id) == 1:
            sql = "select id from future.member where mobilephone='{}'".format(eval(cases.data)['mobilephone'])
            reustl = self.my_msql.read_mysql(sql)
            setattr(TestData, 'loaner_id', reustl['id'])
        self.logger.getlogs('debug', '响应参数：{}'.format(cases.actual))
        allure.attach('{}'.format(eval(cases.expected)), '预期结果')
        allure.attach('{}'.format(cases.actual), '实际结果')
        try:
            assert eval(cases.expected)['status'] == cases.actual['status']
            assert eval(cases.expected)['code'] == cases.actual['code']
            cases.result = 'PASS'
        except AssertionError as e:
            cases.result = 'FAIL'
            raise e
        finally:
            TestLoan.ex.set_write(cases.case_id, resp.text, cases.result)
            allure.attach('{}'.format(cases.result), '断言结果')
            self.logger.getlogs('info', '测试结果：{}'.format(cases.result))

    def teardown_class(self):
        self.request.sessionclose()
        self.my_msql.close_mysql()
        self.logger.getlogs('info', '------------执行完登录接口测试用例------------')

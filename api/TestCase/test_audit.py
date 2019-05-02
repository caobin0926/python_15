from api.comon.httprequest import HttpRequest
from api.comon.do_excel import Excel
from api.comon import paths
import json
import pytest
import allure
from api.comon.Mylogging import Logs
from api.comon.do_re import replace

"""
定义测试审核接口类
"""


@allure.feature('审核接口')
class TestAudit:
    ex = Excel(paths.cases_file, 'audit')
    datas = ex.get_case()

    def setup_class(self):
        self.request = HttpRequest()
        self.logger=Logs('audit')
        self.logger.getlogs('info', '------------开始执行登录接口测试用例------------')

    @pytest.mark.parametrize('case', datas)
    def test_audit(self, case):
        self.logger.getlogs('info', '测试场景：{}'.format(case.title))
        case.data = replace(case.data, paths.gloads_file, 'testdata')
        self.logger.getlogs('debug', '请求参数：{}'.format(case.data))
        reps1 = self.request.request(case.method, case.url, eval(case.data))
        case.actual = json.loads(reps1.text)
        self.logger.getlogs('debug', '响应参数：{}'.format(case.actual))
        allure.attach('{}'.format(case.data), '请求参数')
        allure.attach('{}'.format(eval(case.expected)), '预期结果')
        allure.attach('{}'.format(case.actual), '实际结果')
        try:
            assert eval(case.expected)['status'] == case.actual['status']
            assert eval(case.expected)['code'] == case.actual['code']
            case.result = 'PASS'
        except AssertionError as e:
            case.result = 'FAIL'
            raise e
        finally:
            TestAudit.ex.set_write(case.case_id, reps1.text, case.result)
            allure.attach('{}'.format(case.result), '断言结果')
            self.logger.getlogs('info', '测试结果：{}'.format(case.result))

    def teardown_class(self):
        TestAudit.ex.colse_excel()
        self.request.sessionclose()
        self.logger.getlogs('info', '------------执行完登录接口测试用例------------')

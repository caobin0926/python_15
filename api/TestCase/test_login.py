from api.comon.httprequest import HttpRequest
from api.comon.do_excel import Excel
import json
from api.comon import paths
import pytest
import allure
from api.comon import do_re
from api.comon.Mylogging import Logs


@allure.feature('登录接口')
class TestLogin:
    ex = Excel(paths.cases_file, 'login')
    datas = ex.get_case()

    def setup_class(self):
        self.logger = Logs('login')
        self.logger.getlogs('info', '------------开始执行登录接口测试用例------------')
        self.req_request = HttpRequest()

    @allure.story('登录模块')
    @pytest.mark.parametrize('case', datas)
    def test_login(self, case):
        self.logger.getlogs('info','测试场景：{}'.format(case.title))
        case.data = do_re.replace(case.data, paths.gloads_file, 'testdata')  # 调用正则表达式封装的替换函数

        try:
            self.logger.getlogs('debug','请求参数：{}'.format(case.data))
            req_reqsond = self.req_request.request(case.method, case.url, eval(case.data))
            case.actual = json.loads(req_reqsond.text)
            self.logger.getlogs('debug','响应参数：{}'.format(case.actual))
            allure.attach('{}'.format(case.data), '请求参数')
            allure.attach('{}'.format(eval(case.expected)), '预期结果')
            allure.attach('{}'.format(case.actual), '实际结果')
            assert eval(case.expected) == case.actual
            case.result = 'PASS'

            # print(case.actual)
        except AssertionError as asser:
            case.result = 'FAIL'
        finally:
            TestLogin.ex.set_write(case.case_id, req_reqsond.text, case.result)
            allure.attach('{}'.format(case.result), '断言结果')
            self.logger.getlogs('info', '测试结果：{}'.format(case.result))

    def teardown_class(self):
        self.req_request.sessionclose()
        self.logger.getlogs('info', '------------执行完登录接口测试用例------------')

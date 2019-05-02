from api.comon.httprequest import HttpRequest
from api.comon.do_excel import Excel
import json
from api.comon import paths
import pytest
import allure
from api.comon import do_re
from api.comon.Mylogging import Logs
from colorama import Fore, Style


# 定义一个测试充值接口的类
# @ddt
@allure.feature('充值接口')
class TestRecharge:
    ex1 = Excel(paths.cases_file, 'recharge')
    datas = ex1.get_case()

    def setup_class(self):
        self.logger = Logs('recharge')
        self.logger.getlogs('info', Fore.YELLOW + '------------开始执行测试用例------------')
        self.rep = HttpRequest()

    @allure.story('充值模块')
    @pytest.mark.parametrize('case', datas)
    def test_recharge(self, case):
        self.logger.getlogs('info', Fore.YELLOW + '测试场景：{}'.format(case.title))
        case.data = do_re.replace(case.data, paths.gloads_file, 'testdata')
        self.logger.getlogs('debug', '请求参数：{}'.format(case.data))
        try:
            reqs = self.rep.request(case.method, case.url, eval(case.data))
            case.actual = json.loads(reqs.text)
            # print(reqs.text)
            self.logger.getlogs('debug', '响应参数：{}'.format(case.actual))

            allure.attach('{}'.format(eval(case.expected)), '预期结果')
            allure.attach('{}'.format(case.actual), '实际结果')
            assert eval(case.expected)['status'] == case.actual['status']
            assert eval(case.expected)['code'] == case.actual['code']
            case.result = 'PASS'
        except AssertionError as asser:
            case.result = 'FAIL'
            raise asser
            self.logger.getlogs('error', Fore.RED + '断言失败原因：{}'.format(asser))
        finally:
            TestRecharge.ex1.set_write(case.case_id, reqs.text, case.result)
            allure.attach('{}'.format(case.result), '断言结果')
            self.logger.getlogs('info', '测试结果：{}'.format(case.result))

    def teardown_class(self):
        TestRecharge.ex1.colse_excel()
        self.logger.getlogs('info', Fore.YELLOW + '------------执行完测试用例------------')
        self.rep.sessionclose()

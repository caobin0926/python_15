from api.comon.httprequest import HttpRequest
from api.comon.do_excel import Excel
from api.comon import paths
import json
import pytest
import allure
from api.comon.do_re import replace, TestData
from api.comon.do_mysql import Mysql
from api.comon.Mylogging import Logs
from api.comon.config import ReadConfig

"""
定义测试竞标接口类
"""


@allure.feature('投资接口')
class TestBidloan:
    ex = Excel(paths.cases_file, 'bidLoan')
    datas = ex.get_case()

    def setup_class(self):
        self.request = HttpRequest()
        self.my_sql = Mysql()
        self.resutl = None
        self.log = Logs('Bidloan')  # 实例化log对象
        self.log.getlogs('info', '------------开始执行测试用例------------')

    @allure.story('投资模块')
    @pytest.mark.parametrize('case', datas)
    def test_bidloan(self, case):
        self.log.getlogs('info', '测试场景：{}'.format(case.title))  # 输出日志
        case.data = replace(case.data, paths.gloads_file, 'testdata')
        self.log.getlogs('info', '请求参数：{}'.format(case.data))
        reps1 = self.request.request(case.method, case.url, eval(case.data))  # 发起请求
        case.actual = json.loads(reps1.text)
        allure.attach('{}'.format(eval(case.expected)), '预期结果')
        allure.attach('{}'.format(case.actual), '实际结果')
        self.log.getlogs('info', '响应参数：{}'.format(case.actual))
        if int(case.case_id) == 1:
            sql = "select id from future.member where mobilephone='{}'".format(eval(case.data)['mobilephone'])
            # print(sql)
            self.resutl = self.my_sql.read_mysql(sql)
            # print(self.resutl)
            setattr(TestData, 'loaner_id', self.resutl['id'])
            self.log.getlogs('info', '类属性loaner_id值：{}'.format(TestData.loaner_id))
        if int(case.case_id) == 2:
            sql = "select id from future.member where mobilephone='{}'".format(eval(case.data)['mobilephone'])
            # print(sql)
            self.resutl = self.my_sql.read_mysql(sql)
            # print(self.resutl)
            setattr(TestData, 'invest_id', self.resutl['id'])
        # print('类属性invest_id值：{}'.format(TestData.invest_id))
        if int(case.case_id) == 5 and case.actual['msg'] == '加标成功':
            sql = "select id from  future.loan where memberid='{}'".format(
                eval(case.data)['memberId'])  # 将标的ID写入到TestData类属性loan_id
            print(sql)
            self.resutl = self.my_sql.read_mysql(sql)
            # print(self.resutl)
            setattr(TestData, 'loan_id', self.resutl['id'])
            print('类属性loan_id值：{}'.format(TestData.loan_id))

        try:
            assert eval(case.expected)['status'] == case.actual['status']
            assert eval(case.expected)['code'] == case.actual['code']
            case.result = 'PASS'
            self.log.getlogs('info', '测试结果：{}'.format(case.result))
        except AssertionError as e:
            case.result = 'FAIL'
            self.log.getlogs('info', '测试结果：{}'.format(case.result))
            self.log.getlogs('error', '原因：{}'.format(e))
            raise e
        finally:
            try:
                TestBidloan.ex.set_write(case.case_id, reps1.text, case.result)
            except PermissionError as i:
                self.log.getlogs('error', '原因：{}'.format(i))
            allure.attach('{}'.format(case.result), '断言结果')

    def teardown_class(self):
        self.log.getlogs('info', '------------执行测试用例完成------------')
        self.request.sessionclose()
        self.my_sql.close_mysql()

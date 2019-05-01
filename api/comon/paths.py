import os

basic_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 测试用例路径
cases_file = os.path.join(basic_dir, 'data', 'cases.xlsx')
# 测试报告路径
resport_file = os.path.join(basic_dir, 'resport')
# 环境配置文件开关
gloads_file = os.path.join(basic_dir, 'config', 'gloads.cfg')
# 测试环境配置文件路径
dedug_file = os.path.join(basic_dir, 'config', 'dedug.cfg')
# 真实环境配置文件路径
real_file = os.path.join(basic_dir, 'config', 'real.cfg')
#数据库配置文件路径
msql_file=os.path.join(basic_dir,'config','db.cfg')
# 日志输出配置文件
log_file=os.path.join(basic_dir,'config','log_level.cfg')
# 日志文件
logs_file=os.path.join(basic_dir,'log','logs.txt')


print(resport_file)

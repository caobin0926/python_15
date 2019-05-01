import pymysql
from api.comon.config import ReadConfig
from api.comon import paths

'''
host:数据库IP
port：数据库端口
database：数据库名称
username：用户名
password：密码
定义一个操作数据库的类
'''


class Mysql:
    def __init__(self):
        self.conf = ReadConfig(paths.msql_file)
        self.host = self.conf.get('mysql', 'host')
        self.port = int(self.conf.get('mysql', 'port'))
        self.database = self.conf.get('mysql', 'database')
        self.username = self.conf.get('mysql', 'username')
        self.password = self.conf.get('mysql', 'password')
        self.mysql = pymysql.connect(host=self.host, user=self.username, password=self.password,
                                     database=self.database, port=self.port, charset='utf8')  # 连接数据库
        self.cours = self.mysql.cursor(pymysql.cursors.DictCursor)  # 定义一个游标

    def read_mysql(self, sql):
        self.cours.execute(sql)  # 执行sql
        self.mysql.commit()
        result = self.cours.fetchone()  # 获取查询的所有结果
        return result

    def close_mysql(self):
        self.cours.close()
        self.mysql.close()


if __name__ == '__main__':
    mysql = Mysql()
    sql = "select id from  future.member where mobilephone='15748583986'"
    result = mysql.read_mysql(sql)
    mysql.close_mysql()
    print(result)

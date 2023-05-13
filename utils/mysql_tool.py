# -*- coding:utf-8 -*-
# Author : charlie chen
# Data ：2020/4/4
# desc : 数据库连接，直连和通过跳板机连接

import pymysql
import configparser
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import log_tool
from sshtunnel import SSHTunnelForwarder


class db_connect():
    def __init__(self,db_name):
        '''
        连接数据库初始化工作
        :param db_name: 数据库名称
        '''
        self.connect(db_name)
    
    def read_config(self,db_name):
        # 读取数据库配置
        # 获取配置文件路径
        configDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
        cf = configparser.ConfigParser()  # 生成一个ConfigParser()对象
        cf.read(configDir, encoding='utf-8')  # 读取文件
        print(cf.sections()) # 获取配置文件中的所有section组 即所有的数据库名称
        data = {} # 给数据存储至字典中
        data['host']= cf.get(db_name, 'host')
        data['user']= cf.get(db_name, 'user')
        data['password']= cf.get(db_name, 'password')
        data['database']= cf.get(db_name, 'database') # 数据库名字
        data['port']= int(cf.get(db_name, 'port'))
        return data

    
    def connect(self,db_name):
        '''
        启动一个mysql连接服务
        '''
        # port在connect底层方法中是int类型，所以必须要转
        db_info = self.read_config(db_name)
        try:
            self.conn= pymysql.connect(**db_info,
                charset='utf8'
            )
            self.conn.commit() # 提交事务 若没有提交（库中字段已经向下移位但内容没有写进，可是自动生成的ID会自动增加）
            self.cursor= self.conn.cursor(pymysql.cursors.DictCursor) # 将取回值以字典形式返回（在取游标的时候定义好）
            return True
        except:
            return False

    def get(self, sql):
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except Exception:
            log_tool.MyLog.critical("exec [%s] fail!" % sql)  # 定义特别严重的bug
    
    def colse(self):
        '''
        关闭数据库连接，游标连接
        '''
        self.cursor.close()
        self.conn.close()
        return 

class db_connect_ssh(db_connect):
    def __init__(self, db_name):
        self.connect(db_name)
    
    def connect(self,db_name):
        '''
        重写父类的连接方法，添加了ssh通道连接服务功能
        '''
        db_info = self.read_config(db_name)
        # 链接跳板机ip
        self.server =SSHTunnelForwarder(
            ssh_address_or_host= (db_info['ssh_address_or_host'], 22),
            ssh_pkey= db_info['ssh_pkey'],
            ssh_private_key_password= db_info['ssh_private_key_password'],
            ssh_username= db_info['ssh_username'],
            remote_bind_address=(db_info['host'], int(db_info['port']))
        )
        # 启动服务
        self.server.start()
        print ('start....')
        print ("ssh 链接状态：",db_name,'....',self.server.local_is_up((db_info['host'],int(db_info['port']))))
        
        #获取连接
        try:
            # self.conn = pymysql.connect(host=host, port=int(port), user=user, passwd=passwd, db=db, charset="utf8")
            self.conn = pymysql.connect(
                host='127.0.0.1',
                port=self.server.local_bind_port,
                user=db_info['user'],
                password=db_info['password'],
                database=db_info['database'],
                read_timeout=5,
                write_timeout=10,
                connect_timeout=10,
                charset='utf8',
            )
            self.conn.commit()
            self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
            return True
        except:
            return False

    def read_config(self,db_name):
        # 读取数据库配置
        # 获取配置文件路径
        configDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
        cf = configparser.ConfigParser()  # 生成一个ConfigParser()对象
        cf.read(configDir, encoding='utf-8')  # 读取文件
        print(cf.sections()) # 获取配置文件中的所有section组 即所有的数据库名称
        data = {} # 给数据存储至字典中
        data['user']= cf.get(db_name, 'user')
        data['password']= cf.get(db_name, 'password')
        data['database']= cf.get(db_name, 'database') # 数据库名字
        data['port']= cf.get(db_name, 'port')
        data['ssh_address_or_host']= cf.get(db_name, 'ssh_address_or_host')
        data['host']= cf.get(db_name, 'host')
        data['ssh_pkey']= cf.get(db_name, 'ssh_pkey')
        data['ssh_private_key_password']= cf.get(db_name, 'ssh_private_key_password')
        data['ssh_username']= cf.get(db_name, 'ssh_username')
        return data
    
    def close(self):
        '''
        重写父类的关闭连接方法，因为新增了一个服务功能
        '''
        self.cursor.close()
        self.conn.close()
        if hasattr(self,'server'):
            self.server.stop()
        return False

    def get(self, sql):
        # db_connect.get(self, sql) # 简单的继承父类的方法，维护不方便
        return super().get(sql) # 使用super方法可以直接调用父类方法，并且不用传self值，维护时只需要改变子类后的名称即可




    
if __name__ == "__main__":
    db = db_connect('test')
    res=db.get('select * from test.user;')
    print(res)
    db.colse()
    # db_ssh = db_connect_ssh('talent_pool')
    # res = db_ssh.get("select * from 19_talent limit 1;")
    # print(res)
    # db_ssh.close()

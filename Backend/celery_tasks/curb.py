import pymysql as pymysql
from celery_tasks.async_tasks import cel
from lib.config import read_config


# ************
# 此文件中保存的对数据库的操作
# 其中包括连接，添加，删除，查询操作
# Actions saved on the database in this file
# Including connection, add, delete and query operations
# ************


# 批量添加，删除操作
# Batch add and delete
@cel.task(ignore_result=True)
def update_arr(sql_arr):
    conn = connection()
    cs = conn.cursor()
    for i in range(len(sql_arr)):
        sql = sql_arr[i]
        cs.execute(sql)
        conn.commit()
    cs.close()
    conn.close()


# 添加，删除操作
# Add, delete operation
@cel.task(ignore_result=True)
def update(sql):
    conn = connection()
    cs = conn.cursor()
    cs.execute(sql)
    conn.commit()
    cs.close()
    conn.close()


# 查询操作
# Select operation
@cel.task
def search(sql):
    conn = connection()
    cs = conn.cursor()
    cs.execute(sql)
    d = cs.fetchall()
    cs.close()
    conn.close()
    return d


def a_search(sql):
    conn = connection()
    cs = conn.cursor()
    cs.execute(sql)
    d = cs.fetchall()
    cs.close()
    conn.close()
    return d


# 获取数据库配置
# Get database configuration
def get_config():
    d = read_config('mysql')
    host = d.get('host')
    port = d.get('port')
    user = d.get('user')
    password = d.get('password')
    database = d.get('database')
    charset = d.get('charset')
    arr = (host, port, user, password, database, charset)
    return arr


# 连接数据库
def connection():
    d = read_config('mysql')
    host = d.get('host')
    port = int(d.get('port'))
    user = d.get('user')
    password = d.get('password')
    database = d.get('database')
    charset = d.get('charset')
    conn = pymysql.connect(host=host, port=port, user=user, password=password,
                           database=database,
                           charset=charset)
    #  Check whether the connection is disconnected. If it is disconnected, reconnect it
    conn.ping(reconnect=True)
    return conn

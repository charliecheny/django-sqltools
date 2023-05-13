# coding=utf-8
import pymysql


def connect(db_info):
    try:
        conn = pymysql.connect(
            host=db_info['host'], user=db_info['user'], password=db_info['password'],
            port=db_info['port'], database=db_info['database'],charset='utf8')
        conn.commit()  # 提交事务 若没有提交（库中字段已经向下移位但内容没有写进，可是自动生成的ID会自动增加）
        return conn
    except:
        raise ValueError('链接配置有误，请重新配置数据库连接')


def exec_sql(sql, db_info, params=None,):
    """
    执行sql，例如insert和update
    :param sql: sql语句
    :param params: sql语句参数
    :param db_info: 数据库信息
    """
    with connect(db_info).cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute(sql, params)
    return True


def fetchone_sql(sql, db_info, params=None, flat=False):
    """
    返回一行数据
    :param sql: sql语句
    :param params: sql语句参数
    :param db: Django数据库名
    :param flat: 如果为True，只返回第一个字段值，例如：id
    :return: 例如：(id, 'username', 'first_name')
    """
    with connect(db_info).cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute(sql, params)
        fetchone = cursor.fetchone()
        if fetchone:
            fetchone = fetchone[0] if flat else fetchone
    return fetchone


def fetchone_to_dict(sql, db_info, params=None):
    """
    返回一行数据
    :param sql: sql语句
    :param params: sql语句参数
    :param db: Django数据库名
    :return: 例如：{"id": id, "username": 'username', "first_name": 'first_name'}
    """
    with connect(db_info).cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute(sql, params)
        desc = cursor.description
        row = dict(zip([col[0] for col in desc], cursor.fetchone()))
    return row


def fetchall_sql(sql, db_info, params=None, flat=False):
    """
    返回全部数据
    :param sql: sql语句
    :param params: sql语句参数
    :param db: Django数据库名
    :param flat: 如果为True，只返回每行数据第一个字段值的元组，例如：(id1, id2, id3)
    :return: 例如：[(id, 'username', 'first_name')]
    """
    with connect(db_info).cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute(sql, params)
        fetchall = cursor.fetchall()
        if fetchall:
            fetchall = tuple([o[0] for o in fetchall]) if flat else fetchall
    return fetchall


def fetchall_to_dict(sql, db_info, params=None):
    """
    返回全部数据
    :param sql: sql语句
    :param params: sql语句参数
    :param db: Django数据库名
    :return: 例如：[{"id": id, "username": 'username', "first_name": 'first_name'}]
    """
    with connect(db_info).cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute(sql, params)
        desc = cursor.description
        object_list = [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]

    return object_list





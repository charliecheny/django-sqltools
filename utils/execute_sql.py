# coding=utf-8

from django.db import connections

default_db = 'teach'


def exec_sql(sql, params=None, db=default_db):
    """
    执行sql，例如insert和update
    :param sql: sql语句
    :param params: sql语句参数
    :param db: Django数据库名
    """
    with connections[db].cursor() as cursor:
        cursor.execute(sql, params)
    return True


def fetchone_sql(sql, params=None, db=default_db, flat=False):
    """
    返回一行数据
    :param sql: sql语句
    :param params: sql语句参数
    :param db: Django数据库名
    :param flat: 如果为True，只返回第一个字段值，例如：id
    :return: 例如：(id, 'username', 'first_name')
    """
    with connections[db].cursor() as cursor:
        cursor.execute(sql, params)
        fetchone = cursor.fetchone()
        if fetchone:
            fetchone = fetchone[0] if flat else fetchone
    return fetchone


def fetchone_to_dict(sql, params=None, db=default_db):
    """
    返回一行数据
    :param sql: sql语句
    :param params: sql语句参数
    :param db: Django数据库名
    :return: 例如：{"id": id, "username": 'username', "first_name": 'first_name'}
    """
    with connections[db].cursor() as cursor:
        cursor.execute(sql, params)
        desc = cursor.description
        row = dict(zip([col[0] for col in desc], cursor.fetchone()))
    return row


def fetchall_sql(sql, params=None, db=default_db, flat=False):
    """
    返回全部数据
    :param sql: sql语句
    :param params: sql语句参数
    :param db: Django数据库名
    :param flat: 如果为True，只返回每行数据第一个字段值的元组，例如：(id1, id2, id3)
    :return: 例如：[(id, 'username', 'first_name')]
    """
    with connections[db].cursor() as cursor:
        cursor.execute(sql, params)
        fetchall = cursor.fetchall()
        if fetchall:
            fetchall = tuple([o[0] for o in fetchall]) if flat else fetchall
    return fetchall


def fetchall_to_dict(sql, params=None, db=default_db):
    """
    返回全部数据
    :param sql: sql语句
    :param params: sql语句参数
    :param db: Django数据库名
    :return: 例如：[{"id": id, "username": 'username', "first_name": 'first_name'}]
    """
    with connections[db].cursor() as cursor:
        cursor.execute(sql, params)
        desc = cursor.description
        object_list = [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]

    return object_list





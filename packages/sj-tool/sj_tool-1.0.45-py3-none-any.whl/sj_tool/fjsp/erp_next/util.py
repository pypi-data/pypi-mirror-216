from decimal import Decimal

import pymysql


# 连接到MySQL数据库
def connect_mysql():
    return pymysql.connect(host="192.168.50.73", user="root", password="123", database="_b396709c7d7b26c3")


def select_data_from_table(
    conn, table_name, columns="*", where_clause=None, where_params=None, to_dict=False, dict_key=None
):
    # 创建一个游标对象
    cursor = conn.cursor()

    column_str = str(columns)[1:-1].replace("'", "`") if columns != "*" else "*"

    # 执行查询语句
    query = f"SELECT {column_str} FROM `{table_name}`"
    if where_clause is not None:
        query += "  WHERE  " + where_clause
        cursor.execute(query, where_params)
    else:
        cursor.execute(query)

    if columns == "*":
        columns = [column[0] for column in cursor.description]

    # 获取查询结果
    query_result = cursor.fetchall()

    # 根据父表键来构建，方便直接使用
    if to_dict and dict_key is not None:
        result = {}
        for row in query_result:
            # 创建字典并与列名配对
            row_dict = {columns[i]: _decimal_to_float(value) for i, value in enumerate(row)}
            if row_dict[dict_key] not in result:
                result[row_dict[dict_key]] = [row_dict]
            else:
                result[row_dict[dict_key]].append(row_dict)
    else:
        result = []
        # 遍历结果
        for row in query_result:
            # 创建字典并与列名配对
            row_dict = {columns[i]: _decimal_to_float(value) for i, value in enumerate(row)}
            result.append(row_dict)

    # 关闭游标和数据库连接
    cursor.close()
    return result


def _decimal_to_float(v):
    if isinstance(v, Decimal):
        return float(v)
    return v


def format_date(d):
    return d.strftime("%y-%m-%d")


def format_datetime(d):
    return d.strftime("%y-%m-%d %H:%M:%S")

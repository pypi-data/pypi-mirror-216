from yplib.index import *
import pymysql


# 有关数据库操作的类
def get_connect(db='MoneyKing', user='moneyking_uer', passwd='3^qp3Xqt4bG7', charset='utf8mb4', port=3306, host='192.168.40.230'):
    # return pymysql.connect(db='MoneyKing', user='moneyking_uer', passwd='3^qp3Xqt4bG7', charset="utf8mb4",
    #                        port=3307,
    #                        host='192.168.40.230')
    return pymysql.connect(db=db, user=user, passwd=passwd, charset=charset, port=port, host=host)


# 执行 sql 语句
def exec_sql(db_conn, sql='', commit=True):
    db_cursor = db_conn.cursor()
    if isinstance(sql, list) or isinstance(sql, set):
        for s in sql:
            db_cursor.execute(s)
    else:
        db_cursor.execute(str(sql))
    if commit:
        db_conn.commit()

# print('end')

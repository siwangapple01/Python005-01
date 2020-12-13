
import pymysql
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
import yaml
from datetime import datetime
from dbutils.pooled_db import PooledDB


with open('config.yaml') as file:
    config_dict = yaml.load(file, Loader=yaml.FullLoader)

config_dict.update({
    "port": 3306,
    "charset": "utf8mb4",
    "maxconnections": 0,
    "mincached": 4,
    "maxcached": 0,
    "maxusage": 5,
    "blocking": True
})

spool = PooledDB(pymysql, **config_dict)


def setupConnection():
    conn = spool.connection()
    cur = conn.cursor()

    return conn, cur


def closeConnection(conn, cur):
    cur.close()
    conn.close()


def main():

    conn, cur = setupConnection()

    innerJoinSQL = "SELECT table1._id, table1._name, table2._id, table2._name \
                   FROM table1 INNER JOIN table2 \
                   ON table1._id = table2._id;"
    leftJoinSQL = "SELECT table1._id, table1._name, table2._id, table2._name \
                   FROM table1 LEFT JOIN table2 \
                   ON table1._id = table2._id;"
    rightJoinSQL = "SELECT table1._id, table1._name, table2._id, table2._name \
                   FROM table1 right JOIN table2 \
                   ON table1._id = table2._id;"

    cur.execute(innerJoinSQL)
    innerJoinResult = cur.fetchall()
    cur.execute(leftJoinSQL)
    leftJoinResult = cur.fetchall()
    cur.execute(rightJoinSQL)
    rightJoinResult = cur.fetchall()

    print(innerJoinResult)
    print(leftJoinResult)
    print(rightJoinResult)

    closeConnection(conn, cur)
    # Base.metadata.create_all(engine)

    # table1_row1 = Table1(_id = 1, _name = "table1_table2")
    # table1_row2 = Table1(_id = 2, _name = "table1")

    # table2_row1 = Table2(_id = 1, _name = "table1_table2")
    # table2_row2 = Table2(_id = 3, _name = "table2")

    # session.add_all([table1_row1, table1_row2, table2_row1, table2_row2 ])
    # session.commit()
    # # # session.commit()


if __name__ == "__main__":
    main()

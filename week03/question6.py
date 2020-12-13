import pymysql
from dbutils.pooled_db import PooledDB
import yaml
from datetime import datetime


with open('config.yaml') as file:
    config_dict = yaml.load(file, Loader=yaml.FullLoader)

checkCustomer = "SELECT customer_id from {table} where customer_id = '{customer_id}'"
checkBalance = "SELECT balance from {table} where customer_id = '{customer_id}'"
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


class Error(Exception):
    pass


class NoCustomerFoundError(Error):
    pass


class NoBalanceFoundError(Error):
    print("there are not enough money from transfer from account")
    pass


class FailedToUpdateDBError(Error):
    pass


class NoEnoughBalanceError(Error):
    pass


class Customer:
    def __init__(self, customerId):
        try:
            conn, cur = setupConnection()
            cur.execute(checkCustomer.format(
                table="customer", customer_id=customerId))
            result = cur.fetchall()[0][0]

            if result:
                self.customerId = customerId
            else:
                closeConnection(conn, cur)
                raise NoCustomerFoundError
        except NoCustomerFoundError:
            print("the given customer id is not found from `customer` table")

        try:
            conn, cur = setupConnection()
            cur.execute(checkBalance.format(
                table="customer_balance", customer_id=customerId))
            result = cur.fetchall()[0][0]

            if result:
                self.customer_balance = result
            else:
                closeConnection(conn, cur)
                raise NoBalanceFoundError
        except NoBalanceFoundError:
            print("the given customer id is not found from `customer_balance` table")


class Transfer:
    def __init__(self, fromCustomerId, toCustomerId, amount):
        self.fromCustomer = Customer(fromCustomerId)
        self.toCustomer = Customer(toCustomerId)
        self.amount = amount
        if self.amount > self.fromCustomer.customer_balance:
            raise NoEnoughBalanceError(
                f"no enough monney {self.amount} in customer {self.fromCustomer.customerId}")

    def updateBalance(self):
        try:
            conn, cur = setupConnection()
            currentTime = datetime.now().isoformat()
            fromSQL = f"UPDATE customer_balance SET balance = balance - {self.amount} WHERE customer_id = '{self.fromCustomer.customerId}';"
            toSQL = f"UPDATE customer_balance SET balance = balance - {self.amount} WHERE customer_id = '{self.toCustomer.customerId}';"
            insertSQL = f"INSERT INTO customer_transaction VALUES('{currentTime}', '{self.fromCustomer.customerId}', '{self.toCustomer.customerId}', {self.amount})"

            cur.execute(fromSQL)
            cur.execute(toSQL)
            cur.execute(insertSQL)

            conn.commit()

        except FailedToUpdateDBError:
            conn.rollback()
            print("fail to update dbs, rolling back")

        finally:
            closeConnection(conn, cur)


def main():
    tansferAction = Transfer(1, 2, 200)
    tansferAction.updateBalance()


if __name__ == "__main__":
    main()

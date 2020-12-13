
import pymysql
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


Base = declarative_base()


class Student(Base):
    __tablename__ = 'student'
    user_id = Column(Integer(), primary_key=True)
    user_name = Column(String(50))
    user_age = Column(Integer())
    user_birthday = Column(Date())
    user_gender = Column(String(50))
    user_education = Column(String(50))
    create_on = Column(DateTime(), default=datetime.now)
    update_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return "student(user_id='{self.user_id}', " \
               "user_name={self.user_name})".format(self=self)


def main():
    # 创建表格
    dburl = "mysql+pymysql://user:password@serverip:3306/testdb?charset=utf8mb4"
    engine = create_engine(dburl, echo=False, encoding="utf-8")
    Base.metadat.create_all(engine)

    # 插入数据
    SessionClass = sessionmaker(bind=engine)
    session = SessionClass()

    student_one = Student(user_name="student a", user_age=10,
                          user_birthday="2010-01-01", user_gender="male", user_education="primary")
    student_two = Student(user_id=2, user_name="student b", user_age=10,
                          user_birthday="2010-01-02", user_gender="female", user_education="primary")
    student_three = Student(user_id=3, user_name="student c", user_age=10,
                            user_birthday="2010-01-03", user_gender="male", user_education="primary")

    session.add(student_one)
    session.add(student_two)
    session.add(student_three)
    session.flush()

    session.commit()

    # 查询数据
    for result in session.query(Student):
        print(result)


if __name__ == "__main__":
    main()

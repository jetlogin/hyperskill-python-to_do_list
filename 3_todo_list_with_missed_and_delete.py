# preparing the environment to work with sqlalchemy
from sqlalchemy import create_engine

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    date = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task

Base.metadata.create_all(engine)

from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

# starting the menu

while True:
    print('''
1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit''')
    choice = input()
    if choice == "0":
        print("Bye!")
        break
    elif choice == "5":
        print("Enter task")
        new_name = input()
        print("Enter deadline")
        raw_deadline = input()
        new_deadline = datetime.strptime(raw_deadline, '%Y-%m-%d')
        new_row = Table(task=new_name, date=new_deadline)
        session.add(new_row)
        session.commit()
        print("The task has been added!")
        continue
    elif choice == "6":
        rows = session.query(Table).order_by(Table.date).all()
        if len(rows) == 0:
            print("Nothing to delete!")
            continue
        else:
            print("Choose the number of the task you want to delete:")
            for i in rows:
                num = 1
                print(str(num) + ". " + i.task + ". " + str(i.date.day) + " " + i.date.strftime("%b"))
                num += 1
        to_del = int(input())
        specific_row = rows[to_del - 1]
        session.delete(specific_row)
        session.commit()
        print("The task has been deleted!")

    elif choice == "1":
        today = datetime.today()
        print("Today:", today.day, today.strftime('%b'))
        rows = session.query(Table).filter(Table.date == today.date()).all()
        if len(rows) == 0:
            print("Nothing to do!")
            continue
        else:
            for i in rows:
                print(str(i.id) + ". " + i.task)
            continue
    elif choice == "2":
        for shift in range(0, 7):
            cur_day = datetime.today() + timedelta(days=shift)
            print(cur_day.strftime("%A"), cur_day.day, cur_day.strftime("%b") + ":")
            rows = session.query(Table).filter(Table.date == cur_day.date()).all()
            if len(rows) == 0:
                print("Nothing to do!")
                print("")
            else:
                for i in rows:
                    num = 1
                    print(str(num) + ". " + i.task)
                    num += 1
                    print("")
        continue
    elif choice == "3":
        print("All tasks:")
        rows = session.query(Table).order_by(Table.date).all()
        if len(rows) == 0:
            print("Nothing to do!")
            continue
        else:
            for i in rows:
                num = 1
                print(str(num) + ". " + i.task + ". " + str(i.date.day) + " " + i.date.strftime("%b"))
                num += 1
            continue
    elif choice == "4":
        print("Missed tasks:")
        rows = session.query(Table).filter(Table.date < datetime.today().date()).order_by(Table.date).all()
        if len(rows) == 0:
            print("Nothing is missed!")
            continue
        else:
            for i in rows:
                num = 1
                print(str(num) + ". " + i.task + ". " + str(i.date.day) + " " + i.date.strftime("%b"))
                num += 1
            continue

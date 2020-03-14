import datetime
from Db import db


class Budget:
    def __init__(self, _id, user, from_date, to_date, total, left):
        self._id = _id
        self.user = user
        self.total = total
        self.left = left

        from_date = from_date.split('-')
        to_date = to_date.split('-')

        self.from_date = datetime.date(int(from_date[0]), int(from_date[1]), int(from_date[2]))
        self.to_date = datetime.date(int(to_date[0]), int(to_date[1]), int(to_date[2]))

    def save(self):
        db.budgets.update({'_id': self._id}, {'$set': {'uid': self.user.uid,
                                                       'from_date': self.from_date.strftime('%Y-%m-%d'),
                                                       'to_date': self.to_date.strftime('%Y-%m-%d'),
                                                       'total': self.total,
                                                       'left': self.total}})

    def addTransaction(self, amount, category):
        transaction_collection = db.transactions

        transaction_collection.insert_one({
            'uid': self.user.uid,
            'bid': self._id,
            'amount': amount,
            'category': category,
            'time': datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        })

        self.left -= amount

        self.save()

    def __str__(self):
        return "Budget[{}, {}, {}, {}, {}]".format(self.user.uid, self.from_date, self.to_date, self.total, self.left)

    def __repr__(self):
        return 'Budget({})'.format(self._id)

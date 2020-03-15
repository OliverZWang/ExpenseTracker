import datetime
from Db import db

from Transaction import Transaction


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
                                                       'left': self.left}})

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

    def getTransaction(self, today=False):
        transaction_collection = db.transactions

        if today:
            date = datetime.datetime.date(datetime.datetime.now())
            transactions = transaction_collection.find({'bid': self._id,
                                                        'time': {'$gte': '{}/{:02d}/{:02d} 00:00:00'.format(date.year, date.month, date.day),
                                                                 '$lte': '{}/{:02d}/{:02d} 23:59:59'.format(date.year, date.month, date.day)}})
        else:
            transactions = transaction_collection.find({'bid': self._id})

        results = []

        for tmp in transactions:
            transaction = Transaction(tmp['_id'], self.user, self, tmp['time'], tmp['amount'], tmp['category'])

            results.append(transaction)

        return results

    def __str__(self):
        return "Budget[{}, {}, {}, {}, {}]".format(self.user.uid, self.from_date, self.to_date, self.total, self.left)

    def __repr__(self):
        return 'Budget({})'.format(self._id)

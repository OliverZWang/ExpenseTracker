import datetime


class Transaction:
    def __init__(self, _id, user, budget, time, amount, category):
        # time shoule be YYYY-MM-DD HH:MM:SS

        self._id = _id
        self.user = user
        self.budget = budget
        self.amount = amount
        self.category = category

        time = time.split(' ')
        date = time[0].split('/')
        time = time[1].split(':')

        self.time = datetime.datetime(int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1]), int(time[2]))

    def __str__(self):
        return "Transaction[{}, {}, {}, {}, {}]".format(self.user.uid, self.budget._id, self.time, self.amount, self.category)

    def __repr__(self):
        return 'Transaction({})'.format(self._id)
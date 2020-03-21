import datetime

from Db import db
from Budget import Budget
import Facebook


class User:
    def __init__(self, uid):
        if 'users' not in db.list_collection_names():
            db.users.create_index([('uid', 1)], unique=True)
        
        user_collection = db.users
        
        user = user_collection.find_one({'uid': uid})
        
        if user is None:
            status, first_name, last_name = Facebook.get_user(uid)
            
            if status:
                user_collection.insert_one({
                    'uid': uid,
                    'first_name': first_name,
                    'last_name': last_name,
                    'user_status': "new"
                })

                self.first_name = first_name
                self.last_name = last_name
                self.user_status = "new"
                self.uid = uid

            else:
                user_collection.insert_one({
                    'uid': uid,
                    'first_name': "",
                    'last_name': "",
                    'user_status': "new"
                })

                self.first_name = ""
                self.last_name = ""
                self.user_status = "new"
                self.uid = uid
                
        else:
            self.uid = uid
            self.first_name = user['first_name']
            self.last_name = user['last_name']
            self.user_status = user['user_status']

    def save(self):
        # This is not good for large data
        db.users.update({'uid': self.uid}, {"$set": {'first_name': self.first_name, 
                                                     'last_name': self.last_name,
                                                     'user_status': self.user_status}})

    def get_budgets(self):
        if 'budgets' not in db.list_collection_names():
            db.budgets.create_index([('uid', 1)])

        budget_collection = db.budgets

        results = []

        for result in budget_collection.find({'uid': self.uid}):
            budget = Budget(result['_id'], self, result['from_date'], result['to_date'], result['total'], result['left'])
            
            results.append(budget)

        return results

    def add_budget(self, from_date, to_date, total):
        # from_date and to_date should be datetime.date(YYYY, MM, DD)
        if 'budgets' not in db.list_collection_names():
            db.budgets.create_index([('uid', 1)])

        budget_collection = db.budgets

        budget_collection.insert_one({
            'uid': self.uid,
            'from_date': from_date.strftime('%Y-%m-%d'),
            'to_date': to_date.strftime('%Y-%m-%d'),
            'total': total,
            'left': total
        })

    def add_total(self, total):
        db.budgets.update({'uid': self.uid}, {"$set": {'total': total, 'left': total}})

    def __str__(self):
        return 'User[{}, {}, {}, {}]'.format(self.uid, self.first_name, self.last_name, self.user_status)

    def __repr__(self):
        return 'User({})'.format(self.uid)
        
        
if __name__ == '__main__':
    user = User('3545504232158581')
    
    print(user)

    print(user.get_budgets())
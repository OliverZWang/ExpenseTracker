from Db import db
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
                
                self.uid = uid
                self.first_name = first_name
                self.last_name = last_name
                self.user_status = "new"
                
        else:
            self.uid = uid
            self.first_name = user['first_name']
            self.last_name = user['last_name']
            self.user_status = user['user_status']
            
            
    def __str__(self):
        return 'User[{}, {}, {}]'.format(self.uid, self.first_name, self.last_name)
    
    
    def __repr__(self):
        return 'User({})'.format(self.uid)
        
        
if __name__ == '__main__':
    user = User('3545504232158581')
    
    print(user)
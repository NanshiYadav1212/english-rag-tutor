# app/database/mongodb.py 
""" Temporary MongoDB setup.
     Later real connection string yahan add hoga. """ 
class DummyDB: 
    def __getattr__(self, name):
        # kisi bhi collection ko call karne par error na aaye 
        return {} 
    
# temporary db object 
db = DummyDB()
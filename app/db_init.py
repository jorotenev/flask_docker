import random
from app import db
from app.models import *

"""
prepare the db with more seed data
"""

first_names = ['Gosho', 'Petar', 'Todor']
last_names = ['Petrov', 'Georgiev', 'Ivanov']
for x in range(1, 10):
    u = User()
    u.email = 'asd{0}@gmail.com'.format(x)
    u.name = first_names[random.randint(0, len(first_names)-1)] + ' ' + last_names[random.randint(0, len(last_names)-1)]
    u.password = "password"

    u.confirmed = True
    db.session.add(u)

db.session.commit()

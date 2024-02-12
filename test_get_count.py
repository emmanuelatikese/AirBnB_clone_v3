#!/usr/bin/python3
""" Test .get() and .count() methods
"""
from models import storage
from models.state import State
from models.city  import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


#print(storage.all(Amenity))
#print(storage.all(Amenity).get('Amenity.2480a4f0-ccc6-4c29-9f84-3ce70614cb4a'))
print(storage.all(Review))



#print("All objects: {}".format(storage.count()))
#print("State objects: {}".format(storage.count(State)))

#first_state_id = list(storage.all(State).values())[0].id

#print("First state: {}".format(storage.get(State, first_state_id)))

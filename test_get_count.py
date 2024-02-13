#!/usr/bin/python3
""" Test .get() and .count() methods
"""
from models import storage
from models.state import State
from models.city  import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


#a = storage.all(Amenity)
#print(a)
b = storage.all(Place)


for x in b.values():
	if x.amenities != []:
		print(x.id)
		print('---------')
		a = x.amenities
		print('it amenities')
		for i in a:
			print(i.to_dict())
	print('it ends')
#x = storage.all(Place)
#print(x)
#l = []


#y = Review(name='hotel')
#storage.new(y)


#storage.new(Review(name='hostel'))
#storage.new(Review(name='laundry'))
#storage.new(Review(name='hotel'))

#storage.save()

'''
pl = Place(
        city_id='521a55f4-7d82-47d9-b54c-a76916479545',
        user_id='your_user_id_here',
        name='Cozy Place with Gym',
        description='A cozy place with a gym amenity',
        number_rooms=2,
        number_bathrooms=1,
        max_guest=4,
        price_by_night=120,
        latitude=40.7128,
        longitude=-74.006,
        amenity_ids=['9c364d27-6e48-4757-8bc5-5f022c95cbb2']  # Add the ID of the Gym amenity
    )

storage.new(pl)
storage.save()
'''
'''
for i in x.get('amenity_ids'):
	print(i)
print(l)
print('-----')
#ans = x.get('Place.dc9cba52-d7ed-4ec3-801c-cde2f720f0c6')
#print(ans.to_dict())


print('-----')
print(storage.all(Place).get('Place.927bb33a-1dc1-4151-8d70-7d34b23d7655'))
#print(storage.all(Amenity).get('Amenity.2480a4f0-ccc6-4c29-9f84-3ce70614cb4a'))
#print(storage.all(Review))

#print(storage.all(City))

#print("All objects: {}".format(storage.count()))
#print("State objects: {}".format(storage.count(State)))

#first_state_id = list(storage.all(State).values())[0].id
'''
#print("First state: {}".format(storage.get(State, first_state_id)))

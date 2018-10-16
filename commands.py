from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db', echo=False)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# myFirstRestaurant = Restaurant(name="Pizza Palace")
# session.add(myFirstRestaurant)
# session.commit()

rest = session.query(Restaurant).all()
for r in rest:
    print("id=%d name=%s" % (r.id, r.name))

firstResult = session.query(Restaurant).first()
print(firstResult.name)

menu = session.query(MenuItem).all()
for m in menu:
    #if float(m.price) > 10.00:
    print("id=%d name=%s price=%s" % (m.id, m.name, m.price))

# Change the name of a Menu Item 
veggieBurgers = session.query(MenuItem).filter_by(name = 'Veggie Burger')
for veggieBurger in veggieBurgers:
    print(veggieBurger.id)
    print(veggieBurger.price)
    print(veggieBurger.restaurant.name)
    print("\n")

UrbanVeggieBurger = session.query(MenuItem).filter_by(id = 9).one()
print(UrbanVeggieBurger.id)
print(UrbanVeggieBurger.price)
    
# UrbanVeggieBurger.price = "$2.99"
# session.add(UrbanVeggieBurger)
# session.commit()

for veggieBurger in veggieBurgers:
    if veggieBurger.price != "$2.99":
       veggieBurger.price = "$2.99"
       session.add(veggieBurger)
       session.commit()

for veggieBurger in veggieBurgers:
    print(veggieBurger.id)
    print(veggieBurger.price)
    print(veggieBurger.restaurant.name)
    print("\n")

try:
    spinach = session.query(MenuItem).filter_by(name = "Spinach Ice Cream").one()
    print (spinach.restaurant.name)
    print(spinach.id)
    print(spinach.name)
    print(spinach.price)
    session.delete(spinach)
    session.commit()
except:
    print("Error trying to delete the entry from the database table.")


try:
    spinach = session.query(MenuItem).filter_by(name = "Spinach Ice Cream").one()
    print (spinach.restaurant.name)
    print(spinach.id)
    print(spinach.name)
    print(spinach.price)
except:
    print("Error entry not found")


session.close()
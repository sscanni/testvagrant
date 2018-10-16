import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
#from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class Restaurant(Base):

    __tablename__ = "restaurant"

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

#####insert at the end of file######
# engine = create_engine('sqlite:///:memory:', echo=True)
engine = create_engine('sqlite:///test.db')
Base.metadata.create_all(bind=engine)

###################################################################

# Session = sessionmaker(bind=engine)
# session = Session()

# # Comment out the next three lines unless you are adding a row to the db table.
# myFirstRestaurant = Restaurant(name="Pizza Palace")
# session.add(myFirstRestaurant)
# session.commit()

# r = session.query(Restaurant).all()
# for rest in r:
#     print("id=%d name=%s" % (rest.id, rest.name))

# session.close()
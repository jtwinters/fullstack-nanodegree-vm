import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Restaurant(Base):
#inside Restaurant class
	__tablename__ = 'restaurant'

	name = Column(
		String(80), nullable = False)
	id = Column(
		Integer, primary_key = True)


class MenuItem(Base):
#inside MenuItem class
	__tablename__ = 'menu_item'

	name = Column(String(80), nullable = False)
	id = Column(Integer, primary_key = True)
	description = Column(String(250))
	price = Column(String(8))
	course = Column(String(250))
	restaurant_id = Column(
		Integer, ForeignKey('restaurant.id'))
	restaurant = relationship(Restaurant)

#We added this serialize function to be able to send JSON objects in a 
#serializable format
	@property
	def serialize(self):
		#Returns object data in easily serializable format
		return {
			'name' : self.name,
			'description' : self.description,
			'id' : self.id,
			'price' : self.price,
			'course' : self.course
		}



####insert at end of file##########
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)
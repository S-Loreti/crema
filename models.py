from database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float

class Cafe(Base):
    __tablename__ = 'cafe_data'

    id = Column(Integer, primary_key=True, index= True)
    cafe_name = Column(String)
    cafe_address = Column(String)
    cafe_city = Column(String)
    cafe_state = Column(String)
    cafe_zip = Column(String)
    cafe_phone = Column(String)
    cafe_website = Column(String)
    cafe_hours = Column(String)
    cafe_photo = Column(String)
    capp_photo = Column(String)
    cafe_long = Column(Float)
    cafe_lat = Column(Float)
from sqlalchemy import Column, Integer, String
from database import Base

""" Module for database models """

class URLS(Base):
    """ Contains shortened and original versions of URLs """
    __tablename__ = "shorten_urls"
    id = Column(Integer, primary_key=True, index=True)
    shortened_url = Column(String, unique=True)
    original_url = Column(String, unique=True)
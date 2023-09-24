import os
from sqlalchemy import create_engine, Column
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from .order import Base, Order

db_path = "database/"

# Check if directory exists and create it
if not os.path.exists(db_path):
    os.makedirs(db_path)

# Url to access local database
db_url = 'sqlite:///%s/db.sqlite3' % db_path

# Create engine to connect with database
engine = create_engine(db_url, echo=False)

# Instantiate a section creator with database
Session = sessionmaker(bind=engine)

# Create database if it does not exist
if not database_exists(engine.url):
    create_database(engine.url)

# Create tables if it does not exist
Base.metadata.create_all(engine)

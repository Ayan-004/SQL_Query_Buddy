import sqlalchemy
from sqlalchemy import create_engine, text

DB_URL = 'sqlite:///retail.db'
engine = create_engine(DB_URL)
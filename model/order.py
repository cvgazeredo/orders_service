from sqlalchemy import Column, Integer, Float, DateTime, Boolean
from datetime import datetime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


# Order database
class Order(Base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    stock_symbol = Column(Integer)
    stock_price = Column(Float)
    quantity = Column(Integer)
    created_at = Column(DateTime, default=datetime.now())
    is_sell = Column(Boolean, default=False)



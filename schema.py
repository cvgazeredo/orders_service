from pydantic import BaseModel
from datetime import datetime
from typing import List

from model import Order


# Order Schema
class OrderSchema(BaseModel):
    id: int
    user_id: int
    stock_symbol: str
    stock_price: float
    quantity: int
    created_at: datetime
    is_sell: bool


# Get Order By Id
class GetOrderById(BaseModel):
    id: int



# List Orders Schema
class ListOrdersSchema(BaseModel):
    orders: List[OrderSchema]


# Create Order Schema
class CreateOrderSchema(BaseModel):
    user_id: int
    stock_symbol: str
    quantity: int


class SellStockSchema(BaseModel):
    user_id: int
    stock_symbol: str
    quantity: int


# Error Schema
class ErrorSchema(BaseModel):
    message: str


class FilterOrderByUser(BaseModel):
    user_id: int


# List order detail
def list_order(order: OrderSchema):
    order = {
        "id": order.id,
        "user_id": order.user_id,
        "stock_symbol": order.stock_symbol,
        "stock_price": order.stock_price,
        "quantity": order.quantity,
        "created_at": order.created_at,
        "is_sell": order.is_sell
    }

    return {"Order": order}


# List all orders
def list_orders(orders: List[Order]):
    result = []

    for order in orders:
        result.append({
            "id": order.id,
            "user_id": order.user_id,
            "stock_symbol": order.stock_symbol,
            "stock_price": order.stock_price,
            "quantity": order.quantity,
            "created_at": order.created_at,
            "is_sell": order.is_sell
        })

    return {"Orders": result}

import requests
from flask import redirect, request
from flask_openapi3 import Info, OpenAPI, Tag
from sqlalchemy import func

from model import Session, Order
from helpers import get_user_id_by_auth
from schema import CreateOrderSchema, list_order, ListOrdersSchema, ErrorSchema, OrderSchema, list_orders, \
    SellStockSchema, GetOrderById, FilterOrderByUser

# Application config
info = Info(title="Project Home Broker -  Orders Microservice", version="1.0.0")
app = OpenAPI(__name__, info=info)
app.run(debug=True)

# Tags for documentation
home_tag = Tag(name="Documentation - Order Microservice", description="Select doc: Swagger, Redoc")
order_tag = Tag(name="Orders", description="Details of orders")
order_transactions_tag = Tag(name="Order - Transactions", description="Buy and Sell")


@app.get("/", tags=[home_tag])
def home():
    return redirect('/openapi')


# Get Order by id
@app.get("/order", tags=[order_tag])
def get_order_by_id(query: GetOrderById):
    order_id = query.id

    # Base connection
    session = Session()

    # Get order by id
    order = session.query(Order).filter(Order.id == order_id).first()

    if not order:
        error_message = "Order not found"
        return {"message": error_message}, 404

    return list_order(order), 200


# List of orders
@app.get("/orders", tags=[order_tag],
         responses={"200": ListOrdersSchema, "404": ErrorSchema})
def get_orders():

    # Base connection
    session = Session()

    # Get all orders
    orders = session.query(Order).all()

    if not orders:
        return {"No orders": []}, 200

    return list_orders(orders), 200


# Get orders by user id
@app.get("/order/user", tags=[order_tag],
         responses={"200": ListOrdersSchema, "404": ErrorSchema})
def filter_order_by_user(query: FilterOrderByUser):
    print("Get order by user id reached")
    user_id = query.user_id

    # Check if user exists
    try:
        response_user_id = get_user_id_by_auth(user_id)
        response_user_id.raise_for_status()

    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code
        error_message = {"User Service": "User not found"}

        return error_message, status_code

    except requests.exceptions.ConnectionError:
        return "User Service unavailable", 503

    # Base connection
    session = Session()

    # Check if this user has any transaction
    get_orders_by_user = session.query(Order).filter(Order.user_id == user_id).all()

    return {"User Transactions": list_orders(get_orders_by_user)}


# Place order
@app.post("/order/create", tags=[order_transactions_tag],
          responses={"200": OrderSchema, "404": ErrorSchema})
def create_order(form: CreateOrderSchema, ):
    print("Create order reached")

    user_id = form.user_id

    # Check if user exists
    try:
        response_user_id = get_user_id_by_auth(user_id)
        response_user_id.raise_for_status()

    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code
        error_message = {"User Service": "User not found"}

        return error_message, status_code

    except requests.exceptions.ConnectionError:
        return "User Service unavailable", 503

    # Access Stock Service
    try:
        req = requests.get("http://127.0.0.1:5001/stock", params={"symbol": form.stock_symbol})
        if req.status_code == 404:
            return {"error": "Stock information not available"}

        stock_data = req.json()

    except requests.exceptions.ConnectionError:
        return "Stock Service unavailable"

    order = Order(
        user_id=user_id,
        stock_symbol=stock_data["stock"],
        stock_price=stock_data["price"],
        quantity=form.quantity
    )

    # Create base connection
    session = Session()

    # Add order to table
    session.add(order)
    session.commit()

    # Return message
    return list_order(order), 200


# Sell stock
@app.post("/order/sell", tags=[order_transactions_tag],
          responses={"200": SellStockSchema, "404": ErrorSchema, "400": ErrorSchema})
def sell_stock(form: SellStockSchema):
    print("Sell order reached")

    user_id = form.user_id
    quantity = form.quantity
    stock = form.stock_symbol.upper()

    # Base connection
    session = Session()

    # Check if user exists
    try:
        response_user_id = get_user_id_by_auth(user_id)
        response_user_id.raise_for_status()

    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code
        error_message = {"User Service": "User not found"}

        return error_message, status_code

    except requests.exceptions.ConnectionError:
        return "User Service unavailable", 503

    # Check the current price of stock
    try:
        req = requests.get("http://127.0.0.1:5001/stock", params={"symbol": form.stock_symbol})
        if req.status_code == 404:
            return {"error": "Stock information not available"}, 404

        stock_data = req.json()

    except requests.exceptions.ConnectionError:
        return "Stock Service unavailable"

    # Check whether the user has enough stocks to sell
    # Bought stocks:
    quantity_buy = session.query(func.sum(Order.quantity)).filter(
        Order.is_sell == False,
        Order.stock_symbol == stock,
        Order.user_id == user_id
    ).scalar()

    if quantity_buy is None:
        quantity_buy = 0

    # Sold stocks:
    quantity_sell = session.query(func.sum(Order.quantity)).filter(
        Order.is_sell == True,
        Order.stock_symbol == stock,
        Order.user_id == user_id
    ).scalar()

    if quantity_sell is None:
        quantity_sell = 0

    # Total
    total_quantity = quantity_buy - quantity_sell

    if total_quantity is None or quantity > total_quantity:
        return {"error": f"User do not have enough stocks to sell. User has currently "
                         f"{total_quantity} of {stock} to operate"}, 400

    # Save sell operation
    order_sell = Order(
        user_id=user_id,
        stock_symbol=stock_data["stock"],
        stock_price=stock_data["price"],
        quantity=form.quantity,
        is_sell=True
    )

    # Add operation to table
    session.add(order_sell)
    session.commit()

    # Return message
    return list_order(order_sell), 200


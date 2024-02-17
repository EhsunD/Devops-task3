from fastapi import FastAPI, HTTPException
import requests
import json

app = FastAPI()

SHOP_MICROSERVICE_URL = "http://shop"  # URL of the Shop microservice
ORDER_FILE = "order.json"  # File to store the paid orders

def get_cart(token: str):
    response = requests.post(f"{SHOP_MICROSERVICE_URL}/cart", params={"token": token})
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error retrieving cart from Shop microservice")
    return response.json()

@app.post("/add_order")
def add_order(token: str):
    cart = get_cart(token)
    return {"cart": cart}

@app.post("/pay_order")
def pay_order(token: str):
    cart = get_cart(token)
    # Simulate payment process and mark the order as paid

    # Save the order to the order.json file
    with open(ORDER_FILE, "a") as file:
        order = {"token": token, "cart": cart}
        json.dump(order, file)
        file.write("\n")

    return {"message": "Order has been paid successfully"}

@app.get("/get_orders")
def get_orders():
    orders = []
    with open(ORDER_FILE, "r") as file:
        for line in file:
            order = json.loads(line)
            orders.append(order)
    return {"orders": orders}

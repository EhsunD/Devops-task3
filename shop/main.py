import json
import requests
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

CARTS_FILE = "carts.json"
ACCOUNT_MICROSERVICE_URL = "http://account"


products = [
    {"id": "1", "name": "Product 1", "price": 10.99},
    {"id": "2", "name": "Product 2", "price": 19.99},
    {"id": "3", "name": "Product 3", "price": 7.50},
]


class CartItem(BaseModel):
    item_id: str
    quantity: int


def load_carts_from_file() -> Dict[str, Dict[str, int]]:
    try:
        with open(CARTS_FILE, "r") as file:
            carts = json.load(file)
            return carts
    except FileNotFoundError:
        return {}


def save_carts_to_file(carts: Dict[str, Dict[str, int]]):
    with open(CARTS_FILE, "w") as file:
        json.dump(carts, file)


def check_token(token: str):
    response = requests.post(f"{ACCOUNT_MICROSERVICE_URL}/check_token", json={"token": token})
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Invalid token")
    return response.json()


def get_user_cart(token: str, carts: Dict[str, Dict[str, int]] = Depends(load_carts_from_file)) -> Dict[str, int]:
    if token not in carts:
        carts[token] = {}
    return carts[token]


def is_valid_item(item_id: str) -> bool:
    valid_item_ids = ["1", "2", "3"]
    return item_id in valid_item_ids



import requests



@app.post("/add_to_cart")
def add_to_cart(cart_item: CartItem, token: str, carts: Dict[str, Dict[str, int]] = Depends(load_carts_from_file)):
    # Check if the token is valid
    response = requests.post(f"{ACCOUNT_MICROSERVICE_URL}/check_token", json={"token": token})
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Invalid token")

    # Token is valid, extract the username from the response
    response_data = response.json()
    if not isinstance(response_data, list) or len(response_data) != 1:
        raise HTTPException(status_code=400, detail="Invalid response from account microservice")

    username = response_data[0]

    if not username:
        raise HTTPException(status_code=400, detail="Invalid response from account microservice")

    # Proceed with adding item to cart
    item_id = cart_item.item_id
    quantity = cart_item.quantity

    if username not in carts:
        carts[username] = {}

    user_cart = carts[username]

    if not is_valid_item(item_id):
        raise HTTPException(status_code=400, detail="Invalid item ID")

    # Add logic to check other validation rules if needed

    if item_id in user_cart:
        user_cart[item_id] += quantity
    else:
        user_cart[item_id] = quantity

    save_carts_to_file(carts)  # Save the carts to file

    return {"message": "Item added to cart"}



@app.get("/Items")
def items():
    return products


@app.get("/ItemDetail/{item_ID}")
def details(item_ID: str):
    item = next((item for item in products if item["id"] == item_ID), None)
    if item:
        return item
    else:
        return {"Item Not Found"}


@app.delete("/remove_from_cart")
def remove_from_cart(product_id: str, token: str):
    carts = load_carts_from_file()

    if token not in carts:
        raise HTTPException(status_code=404, detail="Invalid token")

    user_cart = carts[token]

    if product_id not in user_cart:
        raise HTTPException(status_code=404, detail="Product not found in cart")

    del user_cart[product_id]

    save_carts_to_file(carts)

    return {"message": "Product removed from cart"}


@app.post("/cart")
def cart(token: str):
    carts = load_carts_from_file()

    response = requests.post(f"{ACCOUNT_MICROSERVICE_URL}/check_token", json={"token": token})
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Invalid token")

    # Token is valid, extract the username from the response
    response_data = response.json()
    if not isinstance(response_data, list) or len(response_data) != 1:
        raise HTTPException(status_code=400, detail="Invalid response from account microservice")

    username = response_data[0]

    if not username:
        raise HTTPException(status_code=400, detail="Invalid response from account microservice")
    if username not in carts:
        raise HTTPException(status_code=404, detail="Invalid token")

    user_cart = carts[username]

    return user_cart

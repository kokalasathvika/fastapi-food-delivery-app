from math import ceil
from fastapi import FastAPI, Query, Response
from pydantic import BaseModel, Field

app = FastAPI()

# -----------------------------
# In-memory data
# -----------------------------
menu = [
    {"id": 1, "name": "Margherita Pizza", "price": 299, "category": "Pizza", "is_available": True},
    {"id": 2, "name": "Veg Burger", "price": 149, "category": "Burger", "is_available": True},
    {"id": 3, "name": "French Fries", "price": 99, "category": "Snack", "is_available": True},
    {"id": 4, "name": "Cold Coffee", "price": 129, "category": "Drink", "is_available": False},
    {"id": 5, "name": "Chocolate Cake", "price": 199, "category": "Dessert", "is_available": True},
    {"id": 6, "name": "chicken fried rice", "price": 149, "category": "Rice", "is_available": False},
    {"id": 7, "name": "Paneer Biryani", "price": 349, "category": "Biryani", "is_available": True},
    {"id": 8, "name": "Butter chicken", "price": 249, "category": "Curry", "is_available": False},
    {"id": 9, "name": "Jeera rice", "price": 149, "category": "Rice", "is_available": True},
]

orders = []
order_counter = 1
cart = []

# -----------------------------
# Pydantic Models
# -----------------------------
class OrderRequest(BaseModel):
    customer_name: str = Field(..., min_length=2)
    item_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0, le=20)
    delivery_address: str = Field(..., min_length=10)
    order_type: str = "delivery"


class NewMenuItem(BaseModel):
    name: str = Field(..., min_length=2)
    price: int = Field(..., gt=0)
    category: str = Field(..., min_length=2)
    is_available: bool = True


class CheckoutRequest(BaseModel):
    customer_name: str = Field(..., min_length=2)
    delivery_address: str = Field(..., min_length=10)


# -----------------------------
# Helper Functions
# -----------------------------
def find_menu_item(item_id: int):
    for item in menu:
        if item["id"] == item_id:
            return item
    return None


def calculate_bill(price: int, quantity: int, order_type: str):
    total = price * quantity
    if order_type == "delivery":
        total += 30
    return total


def filter_menu_logic(category=None, max_price=None, is_available=None):
    filtered_items = menu

    if category is not None:
        filtered_items = [
            item for item in filtered_items
            if item["category"].lower() == category.lower()
        ]

    if max_price is not None:
        filtered_items = [
            item for item in filtered_items
            if item["price"] <= max_price
        ]

    if is_available is not None:
        filtered_items = [
            item for item in filtered_items
            if item["is_available"] == is_available
        ]

    return filtered_items


# -----------------------------
# Q1 Home Route
# -----------------------------
@app.get("/")
def home():
    return {"message": "Welcome to our EAT FIT Food Delivery"}


# -----------------------------
# Q2 Get All Menu Items
# -----------------------------
@app.get("/menu")
def get_all_menu():
    return {
        "total": len(menu),
        "items": menu
    }


# -----------------------------
# Q4 Get All Orders
# -----------------------------
@app.get("/orders")
def get_all_orders():
    return {
        "total_orders": len(orders),
        "orders": orders
    }


# -----------------------------
# Q5 Menu Summary
# -----------------------------
@app.get("/menu/summary")
def menu_summary():
    total_items = len(menu)
    available_count = sum(1 for item in menu if item["is_available"])
    unavailable_count = total_items - available_count
    categories = list({item["category"] for item in menu})

    return {
        "total_menu_items": total_items,
        "available_items": available_count,
        "unavailable_items": unavailable_count,
        "categories": categories
    }


# -----------------------------
# Q10 Menu Filter
# -----------------------------
@app.get("/menu/filter")
def filter_menu(
    category: str | None = Query(default=None),
    max_price: int | None = Query(default=None),
    is_available: bool | None = Query(default=None)
):
    filtered_items = filter_menu_logic(category, max_price, is_available)
    return {
        "count": len(filtered_items),
        "items": filtered_items
    }


# -----------------------------
# Q16 Menu Search
# -----------------------------
@app.get("/menu/search")
def search_menu(keyword: str):
    keyword = keyword.lower()
    matched_items = [
        item for item in menu
        if keyword in item["name"].lower() or keyword in item["category"].lower()
    ]

    if not matched_items:
        return {"message": "No matching menu items found"}

    return {
        "total_found": len(matched_items),
        "items": matched_items
    }


# -----------------------------
# Q17 Menu Sort
# -----------------------------
@app.get("/menu/sort")
def sort_menu(sort_by: str = "price", order: str = "asc"):
    allowed_sort_fields = ["price", "name", "category"]
    allowed_order_values = ["asc", "desc"]

    if sort_by not in allowed_sort_fields:
        return {"error": "sort_by must be one of ['price', 'name', 'category']"}

    if order not in allowed_order_values:
        return {"error": "order must be 'asc' or 'desc'"}

    reverse_order = True if order == "desc" else False
    sorted_items = sorted(menu, key=lambda item: item[sort_by], reverse=reverse_order)

    return {
        "sort_by": sort_by,
        "order": order,
        "items": sorted_items
    }


# -----------------------------
# Q18 Menu Pagination
# -----------------------------
@app.get("/menu/page")
def paginate_menu(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=3, ge=1, le=10)
):
    total = len(menu)
    total_pages = ceil(total / limit)
    start = (page - 1) * limit
    paginated_items = menu[start:start + limit]

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages,
        "items": paginated_items
    }


# -----------------------------
# Q20 Combined Browse Endpoint
# -----------------------------
@app.get("/menu/browse")
def browse_menu(
    keyword: str | None = Query(default=None),
    sort_by: str = Query(default="price"),
    order: str = Query(default="asc"),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=4, ge=1, le=10)
):
    allowed_sort_fields = ["price", "name", "category"]
    allowed_order_values = ["asc", "desc"]

    items = menu

    # filter
    if keyword is not None:
        keyword_lower = keyword.lower()
        items = [
            item for item in items
            if keyword_lower in item["name"].lower() or keyword_lower in item["category"].lower()
        ]

    # sort
    if sort_by not in allowed_sort_fields:
        return {"error": "sort_by must be one of ['price', 'name', 'category']"}

    if order not in allowed_order_values:
        return {"error": "order must be 'asc' or 'desc'"}

    reverse_order = True if order == "desc" else False
    items = sorted(items, key=lambda item: item[sort_by], reverse=reverse_order)

    # paginate
    total = len(items)
    total_pages = ceil(total / limit) if total > 0 else 1
    start = (page - 1) * limit
    paginated_items = items[start:start + limit]

    return {
        "keyword": keyword,
        "sort_by": sort_by,
        "order": order,
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages,
        "items": paginated_items
    }


# -----------------------------
# Q11 Add New Menu Item
# -----------------------------
@app.post("/menu")
def add_menu_item(item: NewMenuItem, response: Response):
    for existing_item in menu:
        if existing_item["name"].lower() == item.name.lower():
            return {"error": "Menu item with this name already exists"}

    new_item = {
        "id": len(menu) + 1,
        "name": item.name,
        "price": item.price,
        "category": item.category,
        "is_available": item.is_available
    }

    menu.append(new_item)
    response.status_code = 201
    return {
        "message": "Menu item added successfully",
        "item": new_item
    }


# -----------------------------
# Q14 Add To Cart
# -----------------------------
@app.post("/cart/add")
def add_to_cart(item_id: int, quantity: int = 1):
    item = find_menu_item(item_id)

    if item is None:
        return {"error": "Item not found"}

    if item["is_available"] is False:
        return {"error": "Item is currently unavailable"}

    for cart_item in cart:
        if cart_item["item_id"] == item_id:
            cart_item["quantity"] += quantity
            cart_item["total_price"] = cart_item["quantity"] * item["price"]
            return {
                "message": "Item quantity updated in cart",
                "cart_item": cart_item
            }

    new_cart_item = {
        "item_id": item["id"],
        "item_name": item["name"],
        "price": item["price"],
        "quantity": quantity,
        "total_price": item["price"] * quantity
    }

    cart.append(new_cart_item)
    return {
        "message": "Item added to cart",
        "cart_item": new_cart_item
    }


# -----------------------------
# Q14 View Cart
# -----------------------------
@app.get("/cart")
def view_cart():
    grand_total = sum(item["total_price"] for item in cart)
    return {
        "cart_items": cart,
        "grand_total": grand_total
    }


# -----------------------------
# Q15 Checkout Cart
# -----------------------------
@app.post("/cart/checkout")
def checkout_cart(checkout: CheckoutRequest, response: Response):
    global order_counter

    if len(cart) == 0:
        return {"error": "Cart is empty"}

    placed_orders = []
    grand_total = 0

    for cart_item in cart:
        new_order = {
            "order_id": order_counter,
            "customer_name": checkout.customer_name,
            "item_id": cart_item["item_id"],
            "item_name": cart_item["item_name"],
            "quantity": cart_item["quantity"],
            "price_per_item": cart_item["price"],
            "order_type": "delivery",
            "delivery_address": checkout.delivery_address,
            "total_price": cart_item["total_price"] + 30
        }

        orders.append(new_order)
        placed_orders.append(new_order)
        grand_total += new_order["total_price"]
        order_counter += 1

    cart.clear()
    response.status_code = 201

    return {
        "message": "Checkout completed successfully",
        "placed_orders": placed_orders,
        "grand_total": grand_total
    }


# -----------------------------
# Q19 Orders Search
# -----------------------------
@app.get("/orders/search")
def search_orders(customer_name: str):
    customer_name = customer_name.lower()
    matched_orders = [
        order for order in orders
        if customer_name in order["customer_name"].lower()
    ]

    return {
        "total_found": len(matched_orders),
        "orders": matched_orders
    }


# -----------------------------
# Q19 Orders Sort
# -----------------------------
@app.get("/orders/sort")
def sort_orders(order: str = "asc"):
    if order not in ["asc", "desc"]:
        return {"error": "order must be 'asc' or 'desc'"}

    reverse_order = True if order == "desc" else False
    sorted_orders = sorted(orders, key=lambda item: item["total_price"], reverse=reverse_order)

    return {
        "order": order,
        "orders": sorted_orders
    }


# -----------------------------
# Q3 Get Menu Item By ID
# -----------------------------
@app.get("/menu/{item_id}")
def get_menu_item(item_id: int):
    item = find_menu_item(item_id)
    if item:
        return item
    return {"error": "Item not found"}


# -----------------------------
# Q8 Create Order
# -----------------------------
@app.post("/orders")
def create_order(order: OrderRequest):
    global order_counter

    item = find_menu_item(order.item_id)

    if item is None:
        return {"error": "Item not found"}

    if item["is_available"] is False:
        return {"error": "Item is currently unavailable"}

    if order.order_type not in ["delivery", "pickup"]:
        return {"error": "order_type must be either 'delivery' or 'pickup'"}

    total_price = calculate_bill(item["price"], order.quantity, order.order_type)

    new_order = {
        "order_id": order_counter,
        "customer_name": order.customer_name,
        "item_id": order.item_id,
        "item_name": item["name"],
        "quantity": order.quantity,
        "price_per_item": item["price"],
        "order_type": order.order_type,
        "delivery_address": order.delivery_address,
        "total_price": total_price
    }

    orders.append(new_order)
    order_counter += 1

    return {
        "message": "Order placed successfully",
        "order": new_order
    }


# -----------------------------
# Q12 Update Menu Item
# -----------------------------
@app.put("/menu/{item_id}")
def update_menu_item(
    item_id: int,
    price: int | None = Query(default=None),
    is_available: bool | None = Query(default=None)
):
    item = find_menu_item(item_id)

    if item is None:
        return {"error": "Item not found"}

    if price is not None:
        item["price"] = price

    if is_available is not None:
        item["is_available"] = is_available

    return {
        "message": "Menu item updated successfully",
        "item": item
    }


# -----------------------------
# Q13 Delete Menu Item
# -----------------------------
@app.delete("/menu/{item_id}")
def delete_menu_item(item_id: int):
    item = find_menu_item(item_id)

    if item is None:
        return {"error": "Item not found"}

    menu.remove(item)
    return {
        "message": f"{item['name']} deleted successfully"
    }


# -----------------------------
# Q15 Remove One Item From Cart
# -----------------------------
@app.delete("/cart/{item_id}")
def remove_from_cart(item_id: int):
    for cart_item in cart:
        if cart_item["item_id"] == item_id:
            cart.remove(cart_item)
            return {
                "message": f"{cart_item['item_name']} removed from cart"
            }

    return {"error": "Item not found in cart"}
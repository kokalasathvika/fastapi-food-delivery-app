# fastapi-food-delivery-app
# FastAPI Food Delivery App

A backend project built using FastAPI for a Food Delivery App.

## Features
- Home route
- Get all menu items
- Get menu item by ID
- Menu summary
- Orders list
- Create order using Pydantic validation
- Helper functions for item search and bill calculation
- Menu filter with query parameters
- Add new menu item
- Update menu item
- Delete menu item
- Cart add/view/remove
- Cart checkout workflow
- Menu search
- Menu sorting
- Menu pagination
- Orders search
- Orders sort
- Combined browse endpoint

## Tech Stack
- Python
- FastAPI
- Uvicorn
- Pydantic

## Run the Project

1. Create virtual environment:
   python -m venv venv
2.activate virtual environment:
   venv\Scripts\activate
3.Install dependencies :
pip install -r requirements.txt
4.Run server:
uvicorn main:app --reload
5.open swagger UI:
http://127.0.0.1:8000\docs

# 3) Screenshots folder
Q1_home_route.png
Q2_get_all_menu.png
Q3_get_menu_item_valid.png
Q3_get_menu_item_invalid.png
Q4_get_all_orders.png
Q5_menu_summary.png
Q6_pydantic_validation_error.png
Q7_helper_functions_code.png
Q8_create_order_success.png
Q9_order_type_delivery.png
Q9_order_type_pickup.png
Q10_menu_filter.png
Q11_add_menu_item.png
Q12_update_menu_item.png
Q13_delete_menu_item.png
Q14_add_to_cart.png
Q14_view_cart.png
Q15_checkout_success.png
Q16_menu_search.png
Q17_menu_sort.png
Q18_menu_pagination.png
Q19_orders_search_sort.png
Q20_menu_browse.png

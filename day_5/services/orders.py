orders = [
    {
        "id": 1,
        "item": "mobile",
        "quantity": 1
    },
    {
        "id": 2,
        "item": "mobile",
        "quantity": 2
    },
    {
        "id": 3,
        "item": "mobile",
        "quantity": 5
    },
    {
        "id": 4,
        "item": "laptop",
        "quantity": 1
    },
    {
        "id": 5,
        "item": "laptop",
        "quantity": 2
    },
    {
        "id": 6,
        "item": "laptop",
        "quantity": 3
    },
    {
        "id": 7,
        "item": "tablet",
        "quantity": 1
    },
    {
        "id": 8,
        "item": "tablet",
        "quantity": 2
    },
    {
        "id": 9,
        "item": "tablet",
        "quantity": 4
    },
    {
        "id": 10,
        "item": "headphones",
        "quantity": 1
    },
    {
        "id": 11,
        "item": "headphones",
        "quantity": 2
    },
    {
        "id": 12,
        "item": "headphones",
        "quantity": 5
    },
    {
        "id": 13,
        "item": "keyboard",
        "quantity": 1
    },
    {
        "id": 14,
        "item": "keyboard",
        "quantity": 3
    },
    {
        "id": 15,
        "item": "mouse",
        "quantity": 2
    },
    {
        "id": 16,
        "item": "mouse",
        "quantity": 5
    },
    {
        "id": 17,
        "item": "monitor",
        "quantity": 1
    },
    {
        "id": 18,
        "item": "monitor",
        "quantity": 2
    },
    {
        "id": 19,
        "item": "smartwatch",
        "quantity": 1
    },
    {
        "id": 20,
        "item": "smartwatch",
        "quantity": 3
    }
]


async def get_orders_service(search):
    filtered_orders = []

    for order in orders:
        if search is not None:
            if search.lower() not in order["item"].lower():
                continue

        filtered_orders.append(order)

    return filtered_orders


async def get_order_service(order_id):
    for order in orders:
        if order["id"] == order_id:
            return order

    return None


async def create_order_service(order):
    new_id = max(item["id"] for item in orders) + 1
    order_data = order.model_dump()

    new_order = {
        "id": new_id,
        **order_data  # Unpacking the dictionary and adding its key-value pairs to the new_order dictionary
    }

    orders.append(new_order)

    return new_order


async def update_order_service(updateorders):
    for order in orders:
        if order["id"] == updateorders.id:
            order["item"] = updateorders.item
            order["quantity"] = updateorders.quantity

            return order

    return None


async def delete_order_service(order_id):
    for order in orders:
        if order["id"] == order_id:
            orders.remove(order)

            return order

    return None
import os

def map_order_for_salesdrive(order: dict) -> dict:
    crm_api_key = os.getenv("CRM_API_KEY", "").strip('"')

    user_info = order.get("user", {}).get("info", {})
    products = order.get("info", {}).get("busked", [])
    delivery = order.get("delivery", {})
    delivery_raw_meta = delivery.get("meta")
    delivery_meta = delivery_raw_meta if isinstance(delivery_raw_meta, dict) else {}
    delivery_name = delivery.get("name", "").lower()
    delivery_city = delivery.get("city", "")

    # Обработка данных для курьерской доставки
    service_type = "Warehouse"  # по умолчанию отделение
    shipping_address = delivery_city

    delivery_street = delivery.get("address", "")
    delivery_building = delivery.get("b_number", "")
    delivery_flat = delivery.get("apartment", "")

    delivery_warehouse = delivery.get("warehouse", "")

    if "curier" in delivery_name:
        service_type = "Doors"
        street_part = f"вул. {delivery_street}" if delivery_street else ""
        building_part = f"д.{delivery_building}" if delivery_building else ""
        flat_part = f"кв.{delivery_flat}" if delivery_flat else ""
        shipping_address = ", ".join(filter(None, [delivery_city, street_part, building_part, flat_part]))
    elif "urk poshta" in delivery_name:
        service_type = "Warehouse"
        shipping_address = f"{delivery_city}, відділення {delivery_warehouse}"

    # Определяем тип оплаты по order["integrate"]["pay_type"]
    pay_type = order.get("info", {}).get("pay_type")

    try:
        pay_type_int = int(pay_type)
    except (ValueError, TypeError):
        pay_type_int = None

    payment_method_map = {
    1: "Післяплата",
    4: "Оплата карткою (mono)",
    6: "LiqPay"
    }
    payment_method = payment_method_map.get(pay_type_int, str(pay_type) if pay_type else "Не указан")

    mapped_products = []
    for item in products:
        mapped_products.append({
            "id": item.get("article", ""),
            "name": item.get("title", ""),
            "costPerItem": item.get("price", ""),
            "amount": item.get("count", 1),
            "description": "",
            "discount": "",
            "sku": ""
        })

    result = {
        "form": crm_api_key,
        "getResultData": "1",
        "fName": user_info.get("name", ""),
        "lName": user_info.get("surname", ""),
        "mName": "",
        "phone": user_info.get("phone", ""),
        "email": user_info.get("email", ""),
        "company": "",
        "comment": order.get("comment", ""),
        "shipping_method": delivery.get("name", ""),
        "payment_method": payment_method,
        "shipping_address": shipping_address,
        "sajt": "pitaka.ux.im",
        "externalId": str(order.get("id", "")),
        "organizationId": "",
        "shipping_costs": "",
        "products": mapped_products,
        "novaposhta": {
            "ServiceType": service_type if "nova poshta" in delivery_name else "",
            "payer": "",
            "area": "",
            "region": "",
            "city": delivery_city if "nova poshta" in delivery_name else "",
            "cityNameFormat": "full",
            "WarehouseNumber": delivery_warehouse if "nova poshta" in delivery_name and service_type == "Warehouse" else "",
            "Street": delivery_street if service_type == "Doors" and "nova poshta" in delivery_name else "",
            "BuildingNumber": delivery_building if service_type == "Doors" and "nova poshta" in delivery_name else "",
            "Flat": delivery_flat if service_type == "Doors" and "nova poshta" in delivery_name else "",
            "ttn": ""
        },
        "ukrposhta": {
            "ServiceType": service_type if "urk poshta" in delivery_name else "",
            "payer": "",
            "type": "",
            "city": delivery_city if "urk poshta" in delivery_name else "",
            "WarehouseNumber": delivery_warehouse if "urk poshta" in delivery_name else "",
            "Street": "",
            "BuildingNumber": "",
            "Flat": "",
            "ttn": ""
        },
        "rozetka_delivery": {
            "WarehouseNumber": "",
            "payer": "",
            "ttn": ""
        },
        "meest": {
            "ServiceType": "",
            "payer": "",
            "area": "",
            "city": "",
            "WarehouseNumber": "",
            "ttn": ""
        },
        "nePeredzvonuvatiProm": "",
        "pidtverdzuuBezDzvinkaMenedzera": "",
        "tovariPoPeredzamovlennu": "",
        "con_concornijSpisokneZabiraetp2": "",
        "prodex24source_full": "",
        "prodex24source": "",
        "prodex24medium": "",
        "prodex24campaign": "",
        "prodex24content": "",
        "prodex24term": "",
        "prodex24page": ""
    }

    return result

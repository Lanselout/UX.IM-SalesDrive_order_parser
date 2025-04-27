import os

def map_order_for_salesdrive(order: dict) -> dict:
    user_info = order.get("user", {}).get("info", {})
    products = order.get("info", {}).get("busked", [])
    delivery = order.get("delivery", {})
    np_city = delivery.get("meta", {}).get("np_city", {})
    np_warehouse = delivery.get("meta", {}).get("np_warehouse", {})

    # Передача типа оплаты напрямую
    payment_method = str(order.get("pay_type", "")).strip()

    # Маппинг товаров
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

    return {
        "form": os.getenv("CRM_API_KEY", "").strip('"'),
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
        "shipping_address": delivery.get("warehouse", ""),
        "sajt": "pitaka.ux.im",
        "externalId": str(order.get("id", "")),
        "organizationId": "",
        "shipping_costs": "",
        "products": mapped_products,
        "novaposhta": {
            "ServiceType": "Warehouse",
            "payer": "recipient",
            "area": np_city.get("AreaDescription", ""),
            "region": np_city.get("AreaDescriptionRu", ""),
            "city": np_city.get("Description", ""),
            "cityNameFormat": "full",
            "WarehouseNumber": np_warehouse.get("Number", ""),
            "Street": "",
            "BuildingNumber": "",
            "Flat": "",
            "ttn": ""
        },
        "ukrposhta": {
            "ServiceType": "",
            "payer": "",
            "type": "",
            "city": "",
            "WarehouseNumber": "",
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

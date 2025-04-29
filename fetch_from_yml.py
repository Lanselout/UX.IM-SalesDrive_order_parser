import requests
import xml.etree.ElementTree as ET

def fetch_products_from_yml(yml_url: str) -> dict:
    """
    Загружает товары бренда Pitaka из YML-фида.
    Возвращает словарь {sku: {available, price}}.
    """

    try:
        response = requests.get(yml_url)
        response.raise_for_status()

        products_stock = {}

        root = ET.fromstring(response.content)
        offers = root.findall(".//offer")

        for offer in offers:
            sku = offer.attrib.get('id')
            available_attr = offer.attrib.get('available')
            price_tag = offer.find('price')
            vendor_tag = offer.find('vendor')

            # Фильтруем только товары бренда Pitaka
            if vendor_tag is None or vendor_tag.text.strip().lower() != "pitaka":
                continue

            available = (available_attr.lower() == "true") if available_attr else False
            price = float(price_tag.text) if price_tag is not None else 0.0

            products_stock[sku] = {
                "available": available,
                "price": price
            }

        print(f"✅ Загружено товаров бренда Pitaka: {len(products_stock)}")
        return products_stock

    except Exception as e:
        print(f"❌ Ошибка загрузки YML: {e}")
        return {}

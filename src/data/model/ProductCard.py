# class ProductCard:
#     def __init__(self, md5_link, product_name, brand, model, link, last_seen, category, retail, country):
#         self.md5_link = md5_link
#         self.product_name = product_name
#         self.brand = brand
#         self.model = model
#         self.link = link
#         self.last_seen = last_seen
#         self.category = category
#         self.retail = retail
#         self.country = country

#     def __repr__(self):
#         return f"ProductCArd({self.product_name}, {self.brand}, {self.category}, {self.retail})"

from dataclasses import dataclass

@dataclass
class ProductCard:
    md5_link: str
    product_name: str
    brand: str
    model: str
    link: str
    last_seen: str
    category: str
    retail: str
    country: str

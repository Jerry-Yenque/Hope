import requests
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.data.model.Product import Product # type: ignore
from src.data.model.ProductCard import ProductCard
from src.data.model.Category import Category
from src.data.model.Brand import Brand
from src.data.model.Area import Area
from src.data.model.Division import Division
from src.data.model.Feature import Feature
from pprint import pprint
from typing import Optional
import pandas as pd

# from data.mapper.ProductMapper import map_product_to_desired_format



def map_product_to_desired_format(product: Product) -> dict:
    print(type(product))
    return {
        "new_products_id": product.new_products_id,
        "md5_group": product.md5_group,
        "md5_link": product.md5_link,
        "name": product.name,
        "feature_1": product.feature_1['id'] if product.feature_1 else None,
        "feature_2": product.feature_2['id'] if product.feature_2 else None,
        "feature_3": product.feature_3['id'] if product.feature_3 else None,
        "feature_4": product.feature_4['id'] if product.feature_4 else None,
        "feature_5": product.feature_5['id'] if product.feature_5 else None,
        "brand_id": product.brand_id,
        "category_id": product.category_id,
        "created_at": product.created_at,
        "updated_at": product.updated_at,
        "deleted_at": product.deleted_at,
        "taxo_id": product.taxo_id,
        "last_seen": product.last_seen,
        "id": product.id,
        "taxonomy_product": {
            "md5_link": product.taxonomy_product["md5_link"],
            "product_name": product.taxonomy_product["product_name"],
            "last_seen": product.taxonomy_product["last_seen"],
            "country": product.taxonomy_product["country"],
            "category": product.taxonomy_product["category"],
            "retail": product.taxonomy_product["retail"],
            "brand": product.taxonomy_product["brand"],
            "model": product.taxonomy_product["model"],
            "link": product.taxonomy_product["link"]
        },
        "promo": product.promo
    }

def report(df):
    with open("test.js", "w", encoding="utf-8") as file:
        file.write("db.brand.insertMany([\n")
        for _ in range(len(df)):  
            date =  "null" if df[_].deleted_at is None else f'ISODate("{df[_].deleted_at}")'
            line = f'{{id: {df[_].id}, name: "{df[_].name}", created_at: ISODate("{df[_].created_at}"), updated_at: ISODate("{df[_].updated_at}"), deleted_at: {date}}},\n'
            if(df[_].id == 167):
                print(df[_].name)
            # print(line)
            file.write(line)
        file.write("]);\n\n")
        file.write('// load("C:/WorkSpace/Hope/src/data/api/test.js")')
    print("done?")

def format_iso_date(feature: Optional[str]) -> str:
    if feature is None:
        return "null"
    return f'ISODate("{feature}")'

def reportDivision(df):
    df = pd.DataFrame(df)
    with open("test2.js", "w", encoding="utf-8") as file:
        file.write("db.brand.insertMany([\n")
        for _ in range(len(df)):  
            area = df.at[_, 'area']
            area_json = (
                f'{{"id": {area["id"]}, "name": "{area["name"]}", "created_at": {format_iso_date(area["created_at"])}, '
                f'"updated_at": {format_iso_date(area["updated_at"])}, "deleted_at": {format_iso_date(area["deleted_at"])}}}'
            )
            # date =  "null" if df[_].deleted_at is None else f'ISODate("{df[_].deleted_at}")'
            line = f'{{"id": {df.at[_, "id"]}, "name": "{df.at[_, "name"]}", "created_at": {format_iso_date(df.at[_, "created_at"])}, ' \
            f'"updated_at": {format_iso_date(df.at[_, "updated_at"])}, "area_id": {df.at[_, "area_id"]}, "deleted_at": {format_iso_date(df.at[_, "deleted_at"])}, '\
            f'"area": {area_json}}},\n'
            # print(line)
            file.write(line)
        file.write("]);\n\n")
        file.write('// load("C:/WorkSpace/Hope3/src/data/api/test.js")')


def reportCategory(df):
    df = pd.DataFrame(df)
    with open("test.js", "w", encoding="utf-8") as file:
        file.write("db.category.insertMany([\n")
        
        for index in range(len(df)):
            category = df.iloc[index]
            division = category['division']
            area = division['area']
            
            area_json = (
                f'{{"id": {area["id"]}, "name": "{area["name"]}", "created_at": {format_iso_date(area["created_at"])}, '\
                f'"updated_at": {format_iso_date(area["updated_at"])}, "deleted_at": {format_iso_date(area["deleted_at"])}}}'
            )

            division_json = (
                f'{{"id": {division["id"]}, "name": "{division["name"]}", "created_at": {format_iso_date(division["created_at"])}, '\
                f'"updated_at": {format_iso_date(division["updated_at"])}, "area_id": {division["area_id"]}, "deleted_at": {format_iso_date(division["deleted_at"])}, '\
                f'"area": {area_json}}}'
            )
            
            line = (
                f'{{"id": {category["id"]}, "name": "{category["name"]}", "created_at": {format_iso_date(category["created_at"])}, '\
                f'"updated_at": {format_iso_date(category["updated_at"])}, "deleted_at": {format_iso_date(category["deleted_at"])}, "division_id": {category["division_id"]}, '\
                f'"division": {division_json}}},\n'
            )
            
            file.write(line)
        
        file.write("]);\n\n")
        file.write('// load("C:/WorkSpace/Hope3/src/data/api/test.js")')

def escape_quotes(s: str) -> str:
    return s.replace('"', '\\"')

def reportFeature(df):
    df = pd.DataFrame(df)
    with open("featureCollection.js", "w", encoding="utf-8") as file:
        file.write("db.feature.insertMany([\n")
        
        for index in range(len(df)):
            feature = df.iloc[index]
            category = feature['category']
            division = category['division']
            area = division['area']

            area_json = (
                f'{{"id": {area["id"]}, "name": "{area["name"]}", "created_at": {format_iso_date(area["created_at"])}, '\
                f'"updated_at": {format_iso_date(area["updated_at"])}, "deleted_at": {format_iso_date(area["deleted_at"])}}}'
            )

            division_json = (
                f'{{"id": {division["id"]}, "name": "{division["name"]}", "created_at": {format_iso_date(division["created_at"])}, '\
                f'"updated_at": {format_iso_date(division["updated_at"])}, "area_id": {division["area_id"]}, "deleted_at": {format_iso_date(division["deleted_at"])}, '\
                f'"area": {area_json}}}'
            )

            category_json = (
                f'{{"id": {category["id"]}, "name": "{category["name"]}", "created_at": {format_iso_date(category["created_at"])}, '\
                f'"updated_at": {format_iso_date(category["updated_at"])}, "deleted_at": {format_iso_date(category["deleted_at"])}, "division_id": {category["division_id"]}, '\
                f'"division": {division_json}}}'
            )

            line = (
                f'{{"id": {feature["id"]}, "name": "{escape_quotes(feature["name"])}", "created_at": {format_iso_date(feature["created_at"])}, '\
                f'"updated_at": {format_iso_date(feature["updated_at"])}, "deleted_at": {format_iso_date(feature["deleted_at"])}, "category_id": {feature["category_id"]}, '\
                f'"pos": {feature["pos"]}, '\
                f'"category": {category_json}}},\n'
            )
            
            file.write(line)
        
        file.write("]);\n\n")
        file.write('// load("C:/WorkSpace/Hope/featureCollection.js")')

def reportFatherProduct(df: Product):
    df = pd.DataFrame(df)
    
    with open("headphonesCollection.js", "w", encoding="utf-8") as file:
        file.write("db.headphones.insertMany([\n")
        # print("db.headphones.insertMany([\n")
        for _ in range(len(df)):
            product : Product = df.iloc[_]
            feature1 : Feature = product['feature_1']
            feature2 : Feature = product['feature_2']
            feature3 : Feature = product['feature_3']
            feature4 : Feature = product['feature_4']
            feature5 : Feature = product['feature_5']

            taxonomy_product_json = (
                    f'{{"md5_link": "{product.taxonomy_product["md5_link"]}", "product_name": "{escape_quotes(product.taxonomy_product["product_name"])}", "last_seen": {format_iso_date(product.taxonomy_product["last_seen"])}, '\
                    f'"country": "{product.taxonomy_product["country"]}", "category": "{product.taxonomy_product["category"]}", "retail": "{product.taxonomy_product["retail"]}", "brand": "{product.taxonomy_product["brand"]}", '\
                    f'"model": "{product.taxonomy_product["model"]}", "link": "{product.taxonomy_product["link"]}"}}'
                )
        
            line = f'{{"new_products_id": {product.new_products_id}, "md5_group": "{product.md5_group}", "md5_link": "{product.md5_link}", '\
            f'"name": "{escape_quotes(product["name"])}", "feature_1": {format_feature_id(feature1)}, "feature_2": {format_feature_id(feature2)}, "feature_3": {format_feature_id(feature3)}, "feature_4": {format_feature_id(feature4)}, '\
            f'"feature_5": {format_feature_id(feature5)}, "brand_id": {product.brand_id}, "category_id": {product.category_id}, "created_at": {format_iso_date(product.created_at)}, '\
            f'"updated_at": {format_iso_date(product.updated_at)}, "deleted_at": {format_iso_date(product.deleted_at)}, "taxo_id": {product.taxo_id}, "last_seen": {format_iso_date(product.last_seen)}, '\
            f'"id": {product.id}, "taxonomy_product": {taxonomy_product_json}, "promo": "{product.promo}"}},\n'
            # print(line)
            file.write(line)

        file.write("]);\n\n")
        file.write('// load("C:/WorkSpace/Hope/headphonesCollection.js")')

def format_feature_id(feature: Optional[dict]) -> str:
    if feature is None:
        return "null"
    return f'{feature["id"]}'
    

class TaxonomyApi:
    def __init__(self, baseUrl, token) -> None:
        self.baseUrl = baseUrl
        self.token = token

    def auth(self):
        url = f"{self.baseUrl}/new_api/public/user/login"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
    
    def countPendingProducts(self, body):
        url = f"{self.baseUrl}/new_api/public/products/pending/count"
        headers = {
            'Httptoken': f'{self.token}',
            'Content-Type': 'application/json'
        }
        response = requests.post(url, json=body, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def getPendingProducts(self, body):
        url = f"{self.baseUrl}/new_api/public/products/pending"
        headers = {
            'Httptoken': f'{self.token}',
            'Content-Type': 'application/json',
            'Cache-Control': 'no-cache',
            'User-Agent': 'PostmanRuntime/7.40.0',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        }
        response = requests.post(url, json=body, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f'len de data {len(data['data'])}')
            # print(data)
            productCards = [ProductCard(**item) for item in data['data']]
            print(f'productCards len {len(productCards)}')
            return {
                "current_page": data["current_page"],
                "productCards": productCards,
                "first_page_url": data["first_page_url"],
                "from": data["from"],
                "next_page_url": data["next_page_url"],
                "path": data["path"],
                "per_page": data["per_page"],
                "prev_page_url": data["prev_page_url"],
                "to": data["to"]
            }
        else:
            response.raise_for_status()

    # def getTaxonomizados(self, body):
    #     url = f"{self.baseUrl}/new_api/public/products/all"
    #     headers = {
    #         'Httptoken': f'{self.token}',
    #         'Content-Type': 'application/json'
    #     }
    #     response = requests.get(url, json=body, headers=headers)
    #     if response.status_code == 200:
    #         return response.json()
    #     else:
    #         response.raise_for_status()

    def getAllBrands(self, body):
        url = f"{self.baseUrl}/new_api/public/brands/all"
        headers = {
            'Httptoken': f'{self.token}',
            'Content-Type': 'application/json'
        }
        response = requests.post(url, json=body, headers=headers)
        if response.status_code == 200:
            data = response.json()
            brands = [Brand(**item) for item in data['data']]
            return {
                "current_page": data["current_page"],
                "brands": brands,
                "first_page_url": data["first_page_url"],
                "from": data["from"],
                "next_page_url": data["next_page_url"],
                "path": data["path"],
                "per_page": data["per_page"],
                "prev_page_url": data["prev_page_url"],
                "to": data["to"]
            }
        else:
            response.raise_for_status()
    
    def getAllCategories(self, body):
        url = f"{self.baseUrl}/new_api/public/categories/all"
        headers = {
            'Httptoken': f'{self.token}',
            'Content-Type': 'application/json'
        }
        response = requests.post(url, json=body, headers=headers)
        if response.status_code == 200:
            data = response.json()
            categories = [Category(**item) for item in data['data']]
            return {
                "current_page": data["current_page"],
                "categories": categories,
                "first_page_url": data["first_page_url"],
                "from": data["from"],
                "next_page_url": data["next_page_url"],
                "path": data["path"],
                "per_page": data["per_page"],
                "prev_page_url": data["prev_page_url"],
                "to": data["to"]
            }
        else:
            response.raise_for_status()

    def getAllAreas(self, body):
        url = f"{self.baseUrl}/new_api/public/areas/all"
        headers = {
            'Httptoken': f'{self.token}',
            'Content-Type': 'application/json'
        }
        response = requests.post(url, json=body, headers=headers)
        if response.status_code == 200:
            data = response.json()
            areas = [Area(**item) for item in data['data']]
            return {
                "current_page": data["current_page"],
                "areas": areas,
                "first_page_url": data["first_page_url"],
                "from": data["from"],
                "next_page_url": data["next_page_url"],
                "path": data["path"],
                "per_page": data["per_page"],
                "prev_page_url": data["prev_page_url"],
                "to": data["to"]
            }
        else:
            response.raise_for_status()

    def getAllDivisions(self, body):
        url = f"{self.baseUrl}/new_api/public/divisions/all"
        headers = {
            'Httptoken': f'{self.token}',
            'Content-Type': 'application/json'
        }
        response = requests.post(url, json=body, headers=headers)
        if response.status_code == 200:
            data = response.json()
            divisions = [Division(**item) for item in data['data']]
            return {
                "current_page": data["current_page"],
                "divisions": divisions,
                "first_page_url": data["first_page_url"],
                "from": data["from"],
                "next_page_url": data["next_page_url"],
                "path": data["path"],
                "per_page": data["per_page"],
                "prev_page_url": data["prev_page_url"],
                "to": data["to"]
            }
        else:
            response.raise_for_status()

    def getAllCategories(self, body):
        url = f"{self.baseUrl}/new_api/public/categories/all"
        headers = {
            'Httptoken': f'{self.token}',
            'Content-Type': 'application/json'
        }
        response = requests.post(url, json=body, headers=headers)
        if response.status_code == 200:
            data = response.json()
            categories = [Category(**item) for item in data['data']]
            return {
                "current_page": data["current_page"],
                "categories": categories,
                "first_page_url": data["first_page_url"],
                "from": data["from"],
                "next_page_url": data["next_page_url"],
                "path": data["path"],
                "per_page": data["per_page"],
                "prev_page_url": data["prev_page_url"],
                "to": data["to"]
            }
        else:
            response.raise_for_status()


    def getAllFeatures(self, body):
        url = f"{self.baseUrl}/new_api/public/features/all"
        headers = {
            'Httptoken': f'{self.token}',
            'Content-Type': 'application/json'
        }
        response = requests.post(url, json=body, headers=headers)
        if response.status_code == 200:
            data = response.json()
            features = [Feature(**item) for item in data['data']]
            return {
                "current_page": data["current_page"],
                "features": features,
                "first_page_url": data["first_page_url"],
                "from": data["from"],
                "next_page_url": data["next_page_url"],
                "path": data["path"],
                "per_page": data["per_page"],
                "prev_page_url": data["prev_page_url"],
                "to": data["to"]
            }
        else:
            response.raise_for_status()


    def getAllProducts(self, body):
        url = f"{self.baseUrl}/new_api/public/products/all"
        headers = {
            'Httptoken': f'{self.token}',
            'Content-Type': 'application/json'
        }
        response = requests.post(url, json=body, headers=headers)
        if response.status_code == 200:
            data = response.json()
            products = [Product(**item) for item in data['data']]
            return {
                "current_page": data["current_page"],
                "products": products,
                "first_page_url": data["first_page_url"],
                "from": data["from"],
                "next_page_url": data["next_page_url"],
                "path": data["path"],
                "per_page": data["per_page"],
                "prev_page_url": data["prev_page_url"],
                "to": data["to"]
            }
        else:
            response.raise_for_status()

    def taxonomy(self, data: dict):
        url = f"{self.baseUrl}/new_api/public/products"
        headers = {
            'Httptoken': f'{self.token}',
            'Content-Type': 'application/json'
        }
        response = requests.post(url, json=body, headers=headers)





if __name__ == "__main__":

    base_url = ""
    token = ""
    api = TaxonomyApi(base_url, token)

    # body = {
    # "order_by": "id",
    # #"name": "LENOVO",  # para buscar por nombre activa ese campo
    # "asc": 1,
    # "page": 1
    # }

    body = {
  "page": 1,
  "countries": [
    "PE"
  ],
  "retails": [
    "plazavea",
    "tottus",
    "metro",
    "simple-ripley",
    "falabella-pe",
    "lacuracao-pe",
    "oechsle-pe",
    "efe-pe",
    "hiraoka-pe",
    "sodimac-pe",
    "carsa-pe",
    "lg",
    "tailoy-pe",
    "coolbox-pe"
  ],
  "categories": [
    "audifonos",
    "audífonos gamer"
  ],
  "brands": [
    "SONY",
    "JBL",
    "SKULL CANDY",
    "SKULLCANDY",
    "XIAOMI",
    "XIAOMI REDMI",
    "LENOVO",
    "LENOVO / LEMFO",
    "PHILIPS",
    "PHILIPS.",
    "APPLE",
    "HAVIT",
    "BEATS",
    "BEATS BY DR DRE",
    "BEATS BY DR. DRE",
    "BEATS SOLO3",
    "BEATS STUDIO BUDS",
    "BEATS STUDIO3",
    "SAMSUNG",
    "SAMSUNG (AKG)"
  ],
  "start_date": "2024-07-01",
  "end_date": "2024-07-15",
  "name": None,
  "last_seen_products": False
}

    outputData = []
    

    for i in range(1, 2):
        print(f'Page {i}')
        body["page"] = i
        try:
            # print(i)
            outputData.extend(api.getPendingProducts(body)["productCards"])
            # print("Response:", result["brands"])
        except requests.exceptions.RequestException as e:
            print("Error:", e)

    print(f'len : {len(outputData)}')

    for productCard in outputData:
        print(f'"{productCard.product_name}",')





    
    # print(map_product_to_desired_format(outputData[1]))
    # reportFeature(outputData)



## corregí line 22150 id = 467240; 22173 id = 467263  carater ->  "  <-- por --> \" <---
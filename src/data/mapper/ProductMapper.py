from Product import Product

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
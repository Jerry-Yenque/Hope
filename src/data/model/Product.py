from dataclasses import dataclass
from typing import Optional
from src.data.model.Feature import Feature
from src.data.model.Category import Category
from src.data.model.Brand import Brand

@dataclass
class TaxonomyProduct:
    md5_link: str
    product_name: str
    last_seen: str
    country: str
    category: str
    retail: str
    brand: str
    model: str
    link: str

@dataclass
class Product:
    new_products_id: int = None
    md5_group: str = None
    md5_link: str = None
    name: str = None
    feature_1: Feature = None
    feature_2: Feature = None
    feature_3: Feature = None
    feature_4: Optional[Feature] = None
    feature_5: Optional[Feature] = None
    brand_id: int = None
    category_id: int = None
    created_at: str = None
    updated_at: str = None
    deleted_at: Optional[str] = None
    taxo_id: int = None
    last_seen: str = None
    id: int = None
    category: Category = None
    brand: Brand = None
    taxonomy_product: TaxonomyProduct = None
    promo: str = None
    
    def __hash__(self):
        return hash((self.name, self.feature_1, self.feature_2, self.feature_3))
    
    def to_dict(self):
        # Filtrar atributos None y también llamar al método to_dict de la clase Feature si es necesario
        return {k: (v.to_dict() if hasattr(v, 'to_dict') else v) for k, v in self.__dict__.items() if v is not None}
 

# p = Product(new_products_id=None, md5_group=None, md5_link=None, name='AKG TIPO C', feature_1=Feature(id=2551, name='IN EAR', created_at=None, updated_at=None, category_id=None, pos=None, category=None, deleted_at=None), feature_2=Feature(id=2553, name='POR CABLE', created_at=None, updated_at=None, category_id=None, pos=None, category=None, deleted_at=None), feature_3=Feature(id=2555, name='SIN CANCELACIÓN DE RUIDO', created_at=None, updated_at=None, category_id=None, pos=None, category=None, deleted_at=None), feature_4=None, feature_5=None, brand_id=None, category_id=None, created_at=None, updated_at=None, deleted_at=None, taxo_id=None, last_seen=None, id=None, category=None, brand=None, taxonomy_product=None, promo=None)


# print(p.to_dict())

# Ejemplo de uso
# taxonomy_product = TaxonomyProduct(
#     md5_link="29aeee669a44dc4471e11c8c5a1d7821",
#     product_name="AUDIFONOS BLUETOOTH LENOVO LP75 TWS 2022 + MOCHILA LAPTOP USB",
#     last_seen="2024-03-25",
#     country="PE",
#     category="AUDIFONOS",
#     retail="FALABELLA-PE",
#     brand="LENOVO",
#     model="---",
#     link="https://www.falabella.com.pe/falabella-pe/product/118628523/Audifonos-bluetooth-lenovo-lp75-tws-2022-+-mochila-laptop-usb"
# )

# product = ProductDb(
#     new_products_id=242891,
#     md5_group="9dbd88898cd731b3a31e575be9adf6f8",
#     md5_link="29aeee669a44dc4471e11c8c5a1d7821",
#     name="LP75 NEGRO*MOCHILA",
#     id_feature_1=2551,
#     id_feature_2=2552,
#     id_feature_3=2554,
#     id_feature_4=None,
#     id_feature_5=None,
#     brand_id=1372,
#     category_id=36,
#     created_at="2023-05-10T16:56:02.000000Z",
#     updated_at="2023-05-10T16:59:47.000000Z",
#     deleted_at=None,
#     taxo_id=380219168,
#     last_seen="2024-03-25",
#     id=242891,
#     taxonomy_product=taxonomy_product,
#     promo="Ofertec"
# )

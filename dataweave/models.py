from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DECIMAL, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base

#FIXME: Take input via config/environment
DB_URL = 'sqlite:///products.db'

Base = declarative_base()
engine = create_engine(DB_URL)

class MetaInfoModel(Base):
    __tablename__ = 'meta_info'

    id = Column(Integer, primary_key=True)
    #FIXME: This can be another table
    account_code = Column(String(100))
    crawl_page_counter = Column(Integer)
    #FIXME: This can be another table
    postal_zip_code = Column(String(20))
    postal_zip_name = Column(String(100))
    store_code = Column(String(50))
    place_name = Column(String(100))
    admin_name1 = Column(String(100))
    bundle_versions_row_pk_hash = Column(String(100))
    bundle_variant_field_mapping = Column(String)
    bundle_definition = Column(String)
    fulfilment_modes = Column(String)
    seller_name = Column(String(100))
    bundle_match_type = Column(String(50))
    reference_product_id = Column(String(50))
    bundle_definition_hash = Column(String(100))
    #FIXME: This can be int/datetime
    major_version_end_time = Column(String(50))

    product_id = Column(String(50), ForeignKey('products.reference_product_id'))
    product = relationship("ProductModel", back_populates="meta_info")

class ProductModel(Base):
    __tablename__ = 'products'

    reference_product_id = Column(String(50), primary_key=True)
    available_price = Column(DECIMAL(10, 2))
    in_stock = Column(Boolean)
    source = Column(String(100))

    meta_info = relationship("MetaInfoModel", uselist=False, back_populates="product")

def main():
    Base.metadata.create_all(engine)

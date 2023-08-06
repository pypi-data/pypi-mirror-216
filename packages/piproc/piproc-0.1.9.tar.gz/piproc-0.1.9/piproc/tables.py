from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class Processing(Base):
    __tablename__ = 'processing'

    id = Column(String, primary_key=True)
    tile = Column(String)
    lons = Column(String)
    lats = Column(String)
    tile_date = Column(DateTime)
    crs = Column(Integer)
    downloaded = Column(Integer)
    no_downloaded = Column(Integer)
    date_downloaded = Column(DateTime)
    download_path = Column(String)
    indexed = Column(Integer)
    no_indexed = Column(Integer)
    date_indexed = Column(DateTime)
    index_path = Column(String)
    prediction = Column(Integer)
    no_prediction = Column(Integer)
    date_prediction = Column(DateTime)
    pred_path = Column(String)
    model = Column(String)

class Products(Base):
    __tablename__ = 'products'

    id = Column(String, primary_key=True)
    base_id = Column(String)
    tile = Column(String)
    lons = Column(String)
    lats = Column(String)
    tile_date = Column(DateTime)
    crs = Column(Integer)
    prediction = Column(Integer)
    no_prediction = Column(Integer)
    date_prediction = Column(DateTime)
    pred_path = Column(String)
    model = Column(String)
    avg = Column(Float)
    min = Column(Float)
    max = Column(Float)
    std = Column(Float)
    area = Column(Integer)
    length = Column(Float)

class PlanetProc(Base):
    __tablename__ = 'planet_processing'

    id = Column(String, primary_key=True)
    lons = Column(String)
    lats = Column(String)
    tile_date = Column(DateTime)
    crs = Column(Integer)
    downloaded = Column(Integer)
    no_downloaded = Column(Integer)
    date_downloaded = Column(DateTime)
    download_path = Column(String)
    indexed = Column(Integer)
    no_indexed = Column(Integer)
    date_indexed = Column(DateTime)
    index_path = Column(String)
    prediction = Column(Integer)
    no_prediction = Column(Integer)
    date_prediction = Column(DateTime)
    pred_path = Column(String)
    model = Column(String)

class PlanetProd(Base):
    __tablename__ = 'planet_products'

    id = Column(String, primary_key=True)
    base_id = Column(String)
    lons = Column(String)
    lats = Column(String)
    tile_date = Column(DateTime)
    crs = Column(Integer)
    prediction = Column(Integer)
    no_prediction = Column(Integer)
    date_prediction = Column(DateTime)
    pred_path = Column(String)
    model = Column(String)
    avg = Column(Float)
    min = Column(Float)
    max = Column(Float)
    std = Column(Float)
    area = Column(Integer)
    length = Column(Float)
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column, Float, String

# prep the data
raw_model_output = pd.read_csv("similar_images_predictions_2021-01-22_110931.csv")
raw_model_output = raw_model_output.rename(columns={"Unnamed: 0": "IntIndex"})
columns_list = raw_model_output.columns

unique_images = raw_model_output[
    ['similar_image', 'brand', "description", "price", 'image_path', "clothing", 'material', "pattern", "fit", "style",
     "image_path_full"]]
unique_images = unique_images.drop_duplicates()
print(unique_images.size)
print(raw_model_output.size)

# Prep the db tables
engine = create_engine('sqlite:///image_recommender.db', echo=True)
metadata = MetaData()  # Container holding info about the database

image_metadata = Table(
    'image_metadata',
    metadata,
    Column('similar_image', String, primary_key=True),
    Column('brand', String, nullable=True),
    Column("description", String, nullable=True),
    Column("price", Float, nullable=True),
    Column('image_path', String, nullable=True),
    Column('clothing', String, nullable=True),
    Column('material', String, nullable=True),
    Column('pattern', String, nullable=True),
    Column('fit', String, nullable=True),
    Column('style', String, nullable=True),
    Column('image_path_full', String, nullable=False),
)

metadata.create_all(engine)

for t in metadata.sorted_tables:
    print(t.name)

for c in image_metadata.c:
    print(c)

unique_images.to_sql(
    "image_metadata",
    engine,
    if_exists="replace",
    index=False,
    chunksize=500,
    dtype={
        'similar_image': String,
        'brand': String,
        'description': String,
        'price': Float,
        'image_path': String,
        'clothing': String,
        'material': String,
        'pattern': String,
        'fit': String,
        'style': String,
        'image_path_full': String
    }
)


# engine = create_engine('sqlite:///model_output.db', echo=True)
# meta = MetaData()
#
# image_metadata = Table(
#     'image_metadata',
#     meta,
#     Column('similar_image', String),
#     Column('brand', String),
#     Column("description", String),
#     Column("price", Float),
#     Column('image_path', String),
#     Column('clothing', String),
#     Column('material', String),
#     Column('pattern', String),
#     Column('fit', String),
#     Column('style', String),
#     Column('image_path_full', String),
# )
# meta.create_all(engine)
# print(image_metadata.columns.keys())
# conn = engine.connect()
#
# unique_images.to_sql(
#     "image_metadata",
#     engine,
#     if_exists="replace",
#     index=False,
#     chunksize=500,
#     dtype={
#         'similar_image': String,
#         'brand': String,
#         'description': String,
#         'price': Float,
#         'image_path': String,
#         'clothing': String,
#         'material': String,
#         'pattern': String,
#         'fit': String,
#         'style': String,
#         'image_path_full': String
#     }
# )

import pandas as pd
import sqlalchemy as sal
engine = sal.create_engine('sqlite:///image_recommender.db')
conn = engine.connect()

print(engine.table_names())

result = engine.execute("select similar_image from image_metadata")

for row in result:
    print(row)

result.close()
conn.close()

qry1 = pd.read_sql_query('''select * from image_metadata''', con=engine)
df = pd.DataFrame(qry1, columns=['similar_image', 'brand', "description", "price", 'image_path', "clothing", 'material', "pattern", "fit", "style",
     "image_path_full"])

print(df.head())



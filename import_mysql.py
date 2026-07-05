import pandas as pd
from sqlalchemy import create_engine

# Load CSV
df = pd.read_csv("clean_online_retail.csv")

# MySQL Connection
engine = create_engine(
    "mysql+pymysql://root:Yash1693051043@localhost:3306/retail_db"
)

# Import Data
df.to_sql(
    name="retail_sales",
    con=engine,
    if_exists="replace",   # Existing table ko replace karega
    index=False
)

print("✅ Data Imported Successfully!")
print("Rows Imported:", len(df))
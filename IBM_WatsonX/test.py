from utils.utils import init_sqlite_engine
from sqlalchemy import text, create_engine
from sqlalchemy import text
import pandas as pd
engine = create_engine('sqlite:///mydatabase.db', echo=False)  # Switch to file-based SQLite database
conn = engine.connect()
df = pd.read_csv('utils/demo_data.csv')
df.to_sql('sub', conn, if_exists='replace', index=False)
result = conn.execute(text("SELECT id FROM sub")).fetchall()
print(result)
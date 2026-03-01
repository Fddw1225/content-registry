from database import engine
from sqlalchemy import text

with engine.connect() as conn:
    conn.execute(text("DROP TABLE IF EXISTS contents"))
    conn.commit()

print("contents table dropped.")
import sqlite3

db_path = "C:\Users\Kirsten\content-registry-api\registry.db"  # 复制上一步 FastAPI 打印的路径
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tables:", cursor.fetchall())

cursor.execute("PRAGMA table_info(contents);")
print("Contents table columns:", cursor.fetchall())
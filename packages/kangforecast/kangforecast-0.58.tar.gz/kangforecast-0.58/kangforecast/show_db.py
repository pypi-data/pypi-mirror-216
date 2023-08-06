import sqlite3

# 连接到SQLite数据库
conn = sqlite3.connect('festivals_food.db')

# 创建一个Cursor对象
cursor = conn.cursor()

# 查询数据库中的所有表
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tables in the database:")
for table in cursor.fetchall():
    print(table[0])

# 对于每个表，查询其结构及数据
tables = ['FestivalsFood', 'FamilyIncome', 'FamilyProportion','FoodDemand']
for table in tables:
    print(f"\nStructure and data for {table}:")
    # 查询表结构
    cursor.execute(f"PRAGMA table_info({table});")
    print("Structure:")
    for row in cursor.fetchall():
        print(row)
    # 查询表数据
    cursor.execute(f"SELECT * FROM {table};")
    print("Data:")
    for row in cursor.fetchall():
        print(row)

# 关闭连接
conn.close()

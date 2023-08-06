import sqlite3

# 连接到SQLite数据库
conn = sqlite3.connect('festivals_food.db')

# 创建一个Cursor对象
cursor = conn.cursor()

# 查询数据
cursor.execute('SELECT * FROM FestivalsFood')

# 打印结果
for row in cursor.fetchall():
    print(f"For {row[0]} family at {row[1]}, the probability of consuming {row[2]} is {row[3]}")

# 关闭连接
conn.close()

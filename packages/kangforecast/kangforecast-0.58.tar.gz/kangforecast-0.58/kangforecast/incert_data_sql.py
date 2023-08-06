import sqlite3

# 连接到SQLite数据库
conn = sqlite3.connect('festivals_food.db')

# 创建一个Cursor对象
cursor = conn.cursor()

# 插入示例数据
data = [
    ('Family1', 'Festival1', 'Food1', 0.1),
    ('Family1', 'Festival1', 'Food2', 0.2),
    ('Family1', 'Festival2', 'Food1', 0.3),
    ('Family1', 'Festival2', 'Food2', 0.4),
    ('Family2', 'Festival1', 'Food1', 0.5),
    ('Family2', 'Festival1', 'Food2', 0.6),
    ('Family2', 'Festival2', 'Food1', 0.7),
    ('Family2', 'Festival2', 'Food2', 0.8),
]

for row in data:
    cursor.execute('''
        INSERT INTO FestivalsFood (family_type, festival, food, probability)
        VALUES (?, ?, ?, ?)
    ''', row)

# 提交更改并关闭连接
conn.commit()
conn.close()

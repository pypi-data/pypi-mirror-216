import sqlite3

# 连接到SQLite数据库
conn = sqlite3.connect('festivals_food.db')

# 创建一个Cursor对象
cursor = conn.cursor()

# 插入新的数据
ordinary_day_data = [
    ("Family1", "Ordinary Day", "Food1", 0.15),
    ("Family1", "Ordinary Day", "Food2", 0.25),
    ("Family2", "Ordinary Day", "Food1", 0.35),
    ("Family2", "Ordinary Day", "Food2", 0.45),
]
for data in ordinary_day_data:
    cursor.execute('INSERT INTO FestivalsFood VALUES (?, ?, ?, ?)', data)

# 提交更改
conn.commit()

# 关闭连接
conn.close()


import sqlite3

# 连接到SQLite数据库
conn = sqlite3.connect('festivals_food.db')

# 创建一个Cursor对象
cursor = conn.cursor()

# 创建新的表
cursor.execute('CREATE TABLE FamilyIncome (Family TEXT, Income REAL)')

# 插入数据
income_data = [
    ("Family1", 2000),
    ("Family2", 3000),
]
for data in income_data:
    cursor.execute('INSERT INTO FamilyIncome VALUES (?, ?)', data)

# 提交更改
conn.commit()

# 关闭连接
conn.close()


import sqlite3

# 连接到SQLite数据库
conn = sqlite3.connect('festivals_food.db')

# 创建一个Cursor对象
cursor = conn.cursor()

# 创建新的表
cursor.execute('CREATE TABLE FamilyProportion (Family TEXT, Proportion REAL)')

# 插入数据
proportion_data = [
    ("Family1", 0.3),
    ("Family2", 0.7),
]
for data in proportion_data:
    cursor.execute('INSERT INTO FamilyProportion VALUES (?, ?)', data)

# 提交更改
conn.commit()

# 关闭连接
conn.close()




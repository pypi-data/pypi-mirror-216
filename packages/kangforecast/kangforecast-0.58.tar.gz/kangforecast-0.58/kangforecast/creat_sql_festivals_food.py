import sqlite3

# 创建一个SQLite数据库并连接
conn = sqlite3.connect('festivals_food.db')

# 创建一个Cursor对象
cursor = conn.cursor()

# 创建FestivalsFood表
cursor.execute('''
    CREATE TABLE FestivalsFood (
        family_type TEXT,
        festival TEXT,
        food TEXT,
        probability FLOAT
    )
''')

# 提交并关闭连接
conn.commit()
conn.close()

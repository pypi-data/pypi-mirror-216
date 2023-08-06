import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# 连接到SQLite数据库
conn = sqlite3.connect('festivals_food.db')

# 读取FoodDemand表格
df_demand = pd.read_sql_query("SELECT * from FoodDemand", conn)

# 分别获取两种食物和两种家庭类型的需求
df_food1 = df_demand[df_demand['Food'] == 'Food1']
df_food2 = df_demand[df_demand['Food'] == 'Food2']

df_family1 = df_demand[df_demand['Family'] == 'Family1']
df_family2 = df_demand[df_demand['Family'] == 'Family2']

# 创建新的DataFrame，以节日为索引，食物需求为列
df = pd.DataFrame(index=df_demand['Festival'].unique())
df['Food1'] = df_food1.groupby('Festival')['Demand'].sum().values
df['Food2'] = df_food2.groupby('Festival')['Demand'].sum().values
df['Family1'] = df_family1.groupby('Festival')['Demand'].sum().values
df['Family2'] = df_family2.groupby('Festival')['Demand'].sum().values
df['Total'] = df['Food1'] + df['Food2']

# 绘制折线图
plt.figure(figsize=(10,6))
plt.plot(df.index, df['Food1'], label='Food1')
plt.plot(df.index, df['Food2'], label='Food2')
plt.plot(df.index, df['Family1'], label='Family1', linestyle='--')
plt.plot(df.index, df['Family2'], label='Family2', linestyle='--')
plt.plot(df.index, df['Total'], label='Total', linestyle=':')
plt.xlabel('Festival')
plt.ylabel('Demand')
plt.title('Demand for Food1, Food2 and Total Demand on Different Festivals')
plt.legend()
plt.grid(True)
plt.show()

# 关闭连接
conn.close()

# import sqlite3
# import pandas as pd
# import matplotlib.pyplot as plt

# # 连接到SQLite数据库
# conn = sqlite3.connect('festivals_food.db')

# # 读取FoodDemand表格
# df_demand = pd.read_sql_query("SELECT * from FoodDemand", conn)

# # 分别获取两种食物的需求
# df_food1 = df_demand[df_demand['Food'] == 'Food1']
# df_food2 = df_demand[df_demand['Food'] == 'Food2']

# # 创建新的DataFrame，以节日为索引，食物需求为列
# df = pd.DataFrame(index=df_demand['Festival'].unique())
# df['Food1'] = df_food1.groupby('Festival')['Demand'].sum().values
# df['Food2'] = df_food2.groupby('Festival')['Demand'].sum().values

# # 绘制折线图
# plt.figure(figsize=(10,6))
# plt.plot(df.index, df['Food1'], label='Food1')
# plt.plot(df.index, df['Food2'], label='Food2')
# plt.xlabel('Festival')
# plt.ylabel('Demand')
# plt.title('Demand for Food1 and Food2 on Different Festivals')
# plt.legend()
# plt.grid(True)
# plt.show()

# # 关闭连接
# conn.close()

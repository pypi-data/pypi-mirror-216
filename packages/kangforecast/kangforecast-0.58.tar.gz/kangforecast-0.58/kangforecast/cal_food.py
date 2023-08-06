import sqlite3
import pandas as pd

# 连接到SQLite数据库
conn = sqlite3.connect('festivals_food.db')

# 读取各表格
df_food = pd.read_sql_query("SELECT * from FestivalsFood", conn)
df_income = pd.read_sql_query("SELECT * from FamilyIncome", conn)
df_proportion = pd.read_sql_query("SELECT * from FamilyProportion", conn)

# 社区总家庭数
total_households = 100

# 不同日子
days = df_food['festival'].unique()

# 不同食物
foods = df_food['food'].unique()

# 需求计算
for day in days:
    for food in foods:
        demand = 0
        for i, row in df_proportion.iterrows():
            family_type = row['Family']  # Changed 'family' to 'Family'
            proportion = row['Proportion']
            income = df_income.loc[df_income['Family'] == family_type, 'Income'].values[0]
            consumption_probability = df_food.loc[(df_food['family_type'] == family_type) & (df_food['festival'] == day) & (df_food['food'] == food), 'probability'].values[0]
            demand += proportion * total_households * income * consumption_probability
        print(f"The total demand for {food} on {day} is {demand}")


# 需求计算
for day in days:
    for food in foods:
        print(f"On {day}, the demand for {food} is:")
        total_demand = 0
        for i, row in df_proportion.iterrows():
            family_type = row['Family']  # Changed 'family' to 'Family'
            proportion = row['Proportion']
            income = df_income.loc[df_income['Family'] == family_type, 'Income'].values[0]
            consumption_probability = df_food.loc[(df_food['family_type'] == family_type) & (df_food['festival'] == day) & (df_food['food'] == food), 'probability'].values[0]
            demand = proportion * total_households * income * consumption_probability
            total_demand += demand
            print(f"For {family_type} family, the demand is {demand}")
        print(f"The total demand is {total_demand}")
        print("---------")






# 需求计算
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS FoodDemand (Family TEXT, Festival TEXT, Food TEXT, Demand REAL)')
for day in days:
    for food in foods:
        total_demand = 0
        for i, row in df_proportion.iterrows():
            family_type = row['Family']
            proportion = row['Proportion']
            income = df_income.loc[df_income['Family'] == family_type, 'Income'].values[0]
            consumption_probability = df_food.loc[(df_food['family_type'] == family_type) & (df_food['festival'] == day) & (df_food['food'] == food), 'probability'].values[0]
            demand = proportion * total_households * income * consumption_probability
            total_demand += demand
            cursor.execute("INSERT INTO FoodDemand (Family, Festival, Food, Demand) VALUES (?, ?, ?, ?)", (family_type, day, food, demand))
        print("Before INSERT")
        cursor.execute("INSERT INTO FoodDemand (Family, Festival, Food, Demand) VALUES (?, ?, ?, ?)", ('Total', day, food, total_demand))
        print("After INSERT")
conn.commit()

cursor.close()







df_demand = pd.read_sql_query("SELECT * from FoodDemand", conn)
print(df_demand)





# 关闭连接
conn.close()



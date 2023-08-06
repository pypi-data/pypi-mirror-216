import pandas as pd

# 从CSV文件中读取数据
df = pd.read_csv("festivals_food.csv", index_col=0)

# 打印不同节日的食物消费情况
for festival in df.index:
    print(f"For {festival}:")
    for food in df.columns:
        print(f"\tThe probability of consuming {food} is {df.at[festival, food]}")

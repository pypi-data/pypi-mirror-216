import pandas as pd
import kanglib
import numpy as np



def calculate_weighted_value(df, value_columns, weight_column, result_column):
    # 导入kanglib的calculate_weighted_value函数
    return kanglib.calculate_weighted_value(df, value_columns, weight_column, result_column)




# def use_kanglib_calculate_weighted_value():
#     # 创建一个日期范围
#     dates = pd.date_range(start='2022-01-01', periods=365*2)

#     # 创建活动水平DataFrame
#     activity_levels_df = pd.DataFrame({
#         'date': dates,
#         'activity_level': np.random.rand(len(dates))  # 使用numpy的random.rand生成随机数
#     })

#     # 创建权重DataFrame
#     weights_df = pd.DataFrame({
#         'date': dates,
#         'weight': np.random.rand(len(dates))  # 使用numpy的random.rand生成随机数
#     })

#     # 合并这两个DataFrame
#     df = pd.merge(activity_levels_df, weights_df, on='date')

#     # 使用calculate_weighted_value函数
#     df = kanglib.calculate_weighted_value(df, ['activity_level'], 'weight', 'result')

#     # 打印DataFrame
#     print(df)

#     # 绘制结果
#     plt.plot(df['date'], df['result'])
#     plt.title('Weighted Activity Level over Time')
#     plt.xlabel('Date')
#     plt.ylabel('Weighted Activity Level')
#     plt.show()

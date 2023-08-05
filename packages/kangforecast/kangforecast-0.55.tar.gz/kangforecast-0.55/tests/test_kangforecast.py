
import pandas as pd
import numpy as np
import kangforecast


# 创建一些数据
dates = pd.date_range(start='2022-01-01', periods=365*2)
activity_levels_df = pd.DataFrame({
    'date': dates,
    'activity_level': np.random.rand(len(dates))
})
weights_df = pd.DataFrame({
    'date': dates,
    'weight': np.random.rand(len(dates))
})
df = pd.merge(activity_levels_df, weights_df, on='date')

# 使用calculate_weighted_value函数
df = kangforecast.calculate_weighted_value(df, ['activity_level'], 'weight', 'result')

# ...然后你可以继续你的数据处理流程...


print(df)


import matplotlib.pyplot as plt

# Create a figure and a set of subplots
fig, ax = plt.subplots()

# Plot 'date' on x-axis and 'result' on y-axis
ax.plot(df['date'], df['result'])

# Set plot title and labels
ax.set(xlabel='date', ylabel='result',
       title='Weighted Result Over Time')

# Display the plot
plt.show()


# ...省略了其他代码...

# Create a figure and a set of subplots
fig, ax = plt.subplots()

# Plot 'date' on x-axis and 'result' on y-axis
ax.plot(df['date'], df['result'])

# Set plot title and labels
ax.set(xlabel='date', ylabel='result', title='Weighted Result Over Time-From-Docker')

# Save the plot as a file


import os

# ...with this:
output_path = os.path.expanduser("~/1.live_wit_GPT4/code_project/demand_forcast_retail/release_pypi/tests/results/output.png")
fig.savefig(output_path)

# Replace this line...
# fig.savefig("./results/output.png")



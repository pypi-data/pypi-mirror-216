当然可以。让我们通过两个例子来说明这个思路：

例子1：
我们先从一个简单的例子开始。假设我们有一个模块`calculations.py`，它包含一个函数`calculate_average`，该函数接收一个数字列表，并计算其平均值。这个函数不包含任何数据，它只是接收数据并进行处理：

```python
# calculations.py

def calculate_average(numbers):
    return sum(numbers) / len(numbers)
```

然后，我们可以在主程序`main.py`中加载和生成数据，然后调用`calculate_average`函数：

```python
# main.py

from calculations import calculate_average

numbers = [1, 2, 3, 4, 5]  # 这里我们硬编码了数据，但实际上数据可能来自文件、数据库、网络等

average = calculate_average(numbers)
print(f"The average is {average}")
```

例子2：
现在让我们看一个更复杂的例子，涉及到加载和处理数据的专门模块。假设我们有一个模块`data_loader.py`，它包含一个函数`load_data`，该函数从一个CSV文件中加载数据：

```python
# data_loader.py

import pandas as pd

def load_data(filename):
    return pd.read_csv(filename)
```

我们还有一个模块`analysis.py`，它包含一个函数`analyze`，该函数接收一个`pandas` DataFrame，并进行一些分析（例如，计算平均值）：

```python
# analysis.py

def analyze(dataframe):
    return dataframe.mean()
```

然后，在主程序`main.py`中，我们可以首先使用`data_loader.py`模块加载数据，然后使用`analysis.py`模块进行分析：

```python
# main.py

from data_loader import load_data
from analysis import analyze

dataframe = load_data("data.csv")

result = analyze(dataframe)
print(result)
```

文件目录结构如下：

```
.
├── main.py
├── calculations.py
├── data_loader.py
├── analysis.py
└── data.csv
```

这两个例子都遵循了将数据加载和处理与实际的计算逻辑分离的原则。这样的设计可以提高代码的可读性和可维护性，也使得我们更容易进行单元测试。

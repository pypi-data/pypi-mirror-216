import pandas as pd
from kangforecast.data_loader import load_data
from kangforecast.analysis import analyze

def test_analyze():
    data = load_data('data/testdata.csv')
    result = analyze(data)
    assert isinstance(result, pd.Series)  # 我们假设测试通过的条件是analyze函数返回一个pandas Series对象
    print(result)  # 打印分析结果


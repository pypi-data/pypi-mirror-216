
kangforecast - version
v0.13:
- 完成命令格式
- 转移data. 发不包内不含data
- 增加文档
- 清理目录结构。增加result
- 注意后续我们可以设置初始化的文件夹

- 增加一个功能，即要清理-clear-breath_sleep_startagain:clear-clean-sleep-goupgrade
- 就这个名字了


v0.19.
- 完成清理
- try one function- 测试单一的一个模块: python tests/test_kangforecast.py 

- 模块式建造。建立一个简单的模块。1. 数据导入。---> 测试。
- 最终稳定版本发布前，核心的模块，可以封装如kanglib中，
- 持续注意名称的变化。名称即定位，名称即功能。 
- preparedata,

Daker, 本机，相当于两套系统。两个电脑在测试。 

---

V0.40:
## Task -->在 main.py 的基础上，完成三个部分。或者就是两个部分-读取和分析。
先不想写序号。我觉得序号写得更清楚。 序号比文字，更清楚。 

-1.load
-2.process
-3.show
我觉的这个比较清楚。现出第一个版本。 
-
为避免 _ 与. 的混淆， 我们采用中线。 为避免 .与.混淆，我们采用-
因此，我们的三个程序为：
1-load
2-process
3-show

v0.47
-完成测试：
名称修改为更为可读的：
-rw-r--r--   1 kang  staff    76 Jun 19 13:17 m1load.py
-rw-r--r--   1 kang  staff    64 Jun 19 14:31 m2process.py
-rw-r--r--   1 kang  staff    45 Jun 19 14:40 m3show.py
-rw-r--r--   1 kang  staff  1787 Jun 19 14:41 main.py
-并通过 main.py 进行测试
-发布后，通过两种方式测试：
测试1：tests$ python test_m1m2m3.py 
测试2：pytest -s test_pytest_m1m2m3.py

保存备份包：
-rw-r--r--   1 kang  staff    76 Jun 19 13:17 m1load.py
-rw-r--r--   1 kang  staff    64 Jun 19 14:31 m2process.py
-rw-r--r--   1 kang  staff    45 Jun 19 14:40 m3show.py
-rw-r--r--   1 kang  staff  1787 Jun 19 14:41 main.py
保存到根目录下的 ./bk

-保存 v0.48


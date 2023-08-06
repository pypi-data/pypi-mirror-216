python setup.py sdist bdist_wheel
twine upload dist/*
pip install kangforecast

-关于测试

在Python项目中，通常将测试代码放在一个名为"tests"的目录下，这个目录与你的"src"（源代码）目录是平行的。在你的情况下，源代码目录是"kangforecast"，因此你可以创建一个与"kangforecast"平行的新目录，命名为"tests"。如下所示：

```bash
kang@Love-Grace release_pypi$ tree
.
├── README.md
├── build
│   └── bdist.macosx-12-arm64
├── data
│   └── special_dates.csv
├── dist
│   ├── kangforecast-0.1-py3-none-any.whl
│   └── kangforecast-0.1.tar.gz
├── kangforecast
├── tests
├── kangforecast.egg-info
│   ├── PKG-INFO
│   ├── SOURCES.txt
│   ├── dependency_links.txt
│   └── top_level.txt
└── setup.py
```

你可以在"tests"目录中添加你的测试代码。例如，你可以创建一个名为"test_kangforecast.py"的文件。这样，你的测试代码不会被包含在你的发布包（即通过`pip install`安装的包）中，但是它仍然在你的项目结构中，可以方便你进行开发和测试。

然后，你可以使用测试框架（如`pytest`）来运行你的测试。只需在项目根目录下运行命令`pytest`，它会自动查找并运行所有的测试。

当然，你也可以在你的`setup.py`中指定`tests`目录，这样当其他人安装你的包并希望运行测试时，他们可以直接使用`python setup.py test`命令。如果你决定这样做，你可能需要对你的`setup.py`做一些修改，添加一些关于测试的配置。


--- 关于执行顺序。
当你在终端中键入python，操作系统会遍历你的PATH环境变量中的每一个目录，寻找名为python的可执行文件。

PATH是一个包含了多个文件路径的环境变量，各路径之间由冒号:分隔。当你键入命令时，系统会按照PATH中的顺序，从前往后查找每个路径，看看哪个路径中包含了你要执行的命令。

比如你的PATH可能类似这样：/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/X11/bin:/Users/kang/miniconda3/bin。

当你键入python后，系统首先会查看/usr/local/bin目录下是否有python这个可执行文件，如果有，就会运行它。如果没有，就会接着查看/usr/bin，以此类推。只有在前面的路径都没有找到python可执行文件的情况下，才会去查看/Users/kang/miniconda3/bin。

所以，你使用的Python解释器版本是由PATH中的顺序决定的。如果你希望使用Homebrew的Python解释器，你需要确保Homebrew的路径（通常是/usr/local/bin）在PATH中的位置比Miniconda的路径（/Users/kang/miniconda3/bin）靠前。你可以通过修改PATH来改变这个顺序。
------ for Homebrew:
export PATH="/usr/local/bin:$PATH"

source ~/.bashrc

------for conda
conda create -n new_env python=3.11
conda activate new_env
pip install kangforecast

------
您在 kangforecast 包中包含的数据文件无法通过 pip 安装后直接通过文件路径访问。这是因为当一个包被安装时，它的数据文件被存储在一个特定的位置，而不是在您的当前工作目录或相对路径下。

Python 的包分发工具（如 setuptools 或 distutils）提供了一种机制来包括这些数据文件，并在运行时访问它们。这通常是通过在 setup.py 文件中使用 package_data 关键字来实现的。

为了在您的 kangforecast 模块中访问这些数据文件，您需要使用 pkg_resources 模块，这是 setuptools 提供的一个模块。下面是如何使用它来访问您的数据文件的示例：


import pandas as pd
from pkg_resources import resource_filename

# Use resource_filename to get the path to your data file
datafile = resource_filename('kangforecast', 'data/special_dates.csv')

data = pd.read_csv(datafile)
print(data)
这段代码中，resource_filename 函数接收两个参数：包的名字和文件的相对路径（相对于包的路径）。它返回文件在文件系统中的绝对路径。

请注意，要使此代码工作，您需要确保在 setup.py 中正确地设置了 package_data 参数。例如：

python
Copy code
setup(
    ...
    package_data={
        'kangforecast': ['data/*.csv'],
    },
    ...
)
这会将所有 data 目录下的 CSV 文件包括到分发的包中。
----------
从你展示的目录结构来看，data文件夹是在kangforecast目录的外部，而不是作为kangforecast包的一部分。这就是为什么你的安装包没有包含这些数据文件。

要解决这个问题，你应该将data文件夹移动到kangforecast包内，然后重新打包和安装。你可以使用以下命令将data文件夹移动到kangforecast包内：


mv data kangforecast/

----

pip install --no-cache-dir --upgrade kanglib

-----

在Python中，__init__.py文件用于表示其所在的目录应被视为一个Python包，可以包含代码，也可以为空。这个文件会在导入包时首先被执行。如果你没有特殊的初始化代码需要执行，那么这个文件可以是空的。

下面是一个简单的__init__.py文件例子，它什么也不做：

python
Copy code
# This is an empty file.
如果你在包中有某些函数或者类需要导出，你可以在__init__.py文件中指定。例如，假设你有一个叫做forecast.py的模块，其中有一个prepare_data函数，你可以这样写__init__.py：

python
Copy code
from .forecast import prepare_data
然后，你就可以这样导入函数：

python
Copy code
from kangforecast import prepare_data
如果你没有特殊的导出需求，那么一个空的__init__.py文件就足够了。

在你的情况下，你需要在kangforecast目录下创建一个__init__.py文件（如果不存在的话）。然后，你需要确保你的数据文件（special_dates.csv）在kangforecast/data目录下，然后在你的setup.py文件中指定package_data={'kangforecast': ['data/*.csv']}。完成这些后，你应该就可以正确地打包和安装你的kangforecast包，并能够在安装后读取数据文件了。

最后，重新生成新版本的包，你需要更新setup.py中的版本号，比如改为version='0.3'，然后重新运行python setup.py sdist bdist_wheel来生成新的发行版本。
----
you are rght! we got it !!!  kang@Love-Grace release_pypi$ python test_kangforecast.py 
---------print file kangforecast.__file__:

/Users/kang/1.live_wit_GPT4/code_project/demand_forcast_retail/release_pypi/kangforecast/__init__.py
---------

   start_date    end_date             type
0  2022-06-01  2022-06-07         discount
1  2022-12-23  2022-12-26          holiday
2  2022-02-01   2022-02-5  extreme_weather


------为避免冲突，特别是 pip kanglib pip kangforecast 我们使用Docker 并建设镜像
uname -a
cat /etc/os-release

root@64fe8260fc20:/app/demand_forcast_retail/release_pypi# uname -a
Linux 64fe8260fc20 5.15.49-linuxkit-pr #1 SMP PREEMPT Thu May 25 07:27:39 UTC 2023 aarch64 GNU/Linux
root@64fe8260fc20:/app/demand_forcast_retail/release_pypi# cat /etc/os-release
PRETTY_NAME="Debian GNU/Linux 10 (buster)"
NAME="Debian GNU/Linux"
VERSION_ID="10"
VERSION="10 (buster)"
VERSION_CODENAME=buster
ID=debian
HOME_URL="https://www.debian.org/"
SUPPORT_URL="https://www.debian.org/support"
BUG_REPORT_URL="https://bugs.debian.org/"
-------
我们的系统是PRETTY_NAME="Debian GNU/Linux 10 (buster)" 稳定的linux 10. 


-------1. 完成数据准备。2. 数据处理  3. 数据展示。

---test_activity_special_date_v2.py  这个程序是可以用的。
-------- 2023.6.19
- 1. 给出完整的思路。 ---明确几个模块-先把大模块搭起来。测试一下。
- 2. 完整模块，而后进入一个问题。把每个问题梳理一下-完成子模块
- 给出    几个要点和思路。
首先需要一个大框架。- 1. 读取数据。2. 分析数据。 3. 结果数据（包括可视化）
from kangforecast.data_loader import load_data
from kangforecast.data_analysis import analyze

def main():
    dataframe = load_data("data/testdata.csv")
    result = analyze(dataframe)
    print(result)

if __name__ == "__main__":
    main()


kang@Love-Grace release_pypi$ cat kangforecast/data_loader.py 
import pandas as pd

def load_data(filename):
    return pd.read_csv(filename)
kang@Love-Grace release_pypi$ cat kangforecast/data_analysis.py 
def analyze(dataframe):
    return dataframe.mean()

---problem:关于再次无法找到哦No module named 'kangforecast'
很可能 pip  与 python 两个渠道不一致。 需要查看下。 

which python
/usr/local/bin/python

kang@Love-Grace release_pypi$ pip show kangforecast
Location: /usr/local/lib/python3.11/site-packages
Name: kangforecast
Version: 0.17

kang@Love-Grace release_pypi$ python -m pip show kangforecast
Name: kangforecast
Version: 0.1
Summary: A simple forecast package.
Home-page: https://www.linkedin.com/in/xiaowenkang/
Author: Xiaowen Kang
Author-email: kangxiaowen@gmail.com
License: 
Location: /Users/kang/Library/Python/3.8/lib/python/site-packages

----
问题：
kang@Love-Grace release_pypi$ pip show kangforecast
Location: /usr/local/lib/python3.11/site-packages
Name: kangforecast
Version: 0.17

kang@Love-Grace release_pypi$ python -m pip show kangforecast
Name: kangforecast
Version: 0.1
Summary: A simple forecast package.
Home-page: https://www.linkedin.com/in/xiaowenkang/
Author: Xiaowen Kang
Author-email: kangxiaowen@gmail.com
License: 
Location: /Users/kang/Library/Python/3.8/lib/python/site-packages
----两个语句 相差了一个 -m   为何位置 和版本都不一样？ 

`python -m pip` 和 `pip` 在命令行中输入可能会指向不同的Python环境，这取决于你的系统设置和Python环境配置。

`pip` 通常指向你的系统默认Python环境或者是在你的环境变量中设定的Python环境。在某些系统中，`pip` 可能会默认指向Python 2，尽管你的系统默认的Python版本可能已经是Python 3。

`python -m pip` 会用 `python` 指向的Python解释器来运行pip模块。`python` 在你的系统中可能已经被设定为指向一个特定的Python版本，或者是你当前激活的虚拟环境的Python解释器。

所以当你用 `pip show` 和 `python -m pip show` 的时候，可能会查找到两个不同的Python环境中的包，所以它们的版本和位置可能会不一样。 

一个解决这个问题的办法是始终在指定的Python环境中使用 `python -m pip` 来安装和管理你的Python包，以避免环境混淆。或者，你可以使用Python的虚拟环境（如venv或conda）来为每个项目创建一个独立的环境，这样可以确保你的项目环境中的包版本和依赖关系的一致性。
---- 解决方案：
kang@Love-Grace release_pypi$ which python
/usr/local/bin/python
或者：
kang@Love-Grace release_pypi$ python --version
Python 3.8.0

python3 -m pip install kangforecast
或者：
python3.8 -m pip install kangforecast

从你提供的信息来看，kangforecast已经成功安装到Python 3.8版本中。你的Python 3.8环境中的kangforecast版本为0.17，这与你期望的版本一致。
其中，Defaulting to user installation because normal site-packages is not writeable这条信息表明，pip无法在全局site-packages目录下安装包，因此默认安装到用户级别的site-packages目录。这通常不会造成问题。
然而，你的Python环境出现了一些异常的分发情况（"Ignoring invalid distribution"的警告）。这可能是由于某些包安装或卸载时遇到的问题，或者你的Python环境有些混乱。你可以考虑清理或修复这些问题，以确保你的Python环境的正常工作。如果你不确定如何进行，可能需要寻求专业的技术支持。
-- --> 我们争取统一到 Python 3.8.0 的版本中。
-第一我希望删除旧版本的kangforecast。 因为过去我们曾经出现了这个情况：pi$ /usr/local/bin/python -m pip install kangforecast
DEPRECATION: Python 2.7 will reach the end of its life on January 1st, 2020. Please upgrade your Python as Python 2.7 won't be maintained after that date. A future version of pip will drop support for Python 2.7.
Requirement already satisfied: kangforecast in /usr/local/lib/python2.7/site-packages (0.1)--我们先删除这个版本
-
/usr/local/bin/python -m pip uninstall kangforecast

---> export PATH="/Users/kang/Library/Python/3.8/bin:$PATH"
 echo $SHELL
/bin/bash
Mac中 以这个版本为准 ~/.bash_profile 
-
# Setting PATH
export PATH="/usr/local/bin:$PATH"  # Homebrew Python interpreter  -移动到最后，最后执行，收官有效。因此后续都是优先执行。
export PATH="/Users/kang/Library/Python/3.8/bin:$PATH"
 我们出现了两个这样的路径，是否会冲突？
-不会产生冲突，但会有一个优先级的概念。
你的系统会按照`PATH`环境变量中的顺序去查找命令。如果在一个路径中找到了匹配的命令，系统就会停止进一步搜索，并执行找到的命令。
在你的例子中，`/Users/kang/Library/Python/3.8/bin`被添加到了`PATH`环境变量的开头，所以系统会优先在这个路径中查找命令。只有当在这个路径中没有找到匹配的命令时，系统才会继续在`/usr/local/bin`这个路径中查找。
所以，这种设置并不会产生冲突，但是会改变命令的查找顺序。如果两个路径中都有同样的命令，那么系统将会执行先找到的那一个。
----

解释- 这个内容比较多，我发布一个Blog 方便自己记忆和查询： 主要内容为： python python3  aline别名 路径 pip pip3 以及冲突。以及库的存储
更新在：https://williampolicy.github.io/blog/
https://williampolicy.github.io/blog/2023/Python-and-Pip_version_alias_syspath/
已发布。这样我就弄明白了这些关系了。 
--------- 很清楚，非常好！【solved path problem】 (有了这个解决方案，我暂时不需要 docker，尽管我可以做，但是目前我就用本机，避免复杂)
在 main.py 的基础上，完成三个部分。或者就是两个部分-读取和分析。
先不想写序号。我觉得序号写得更清楚。 序号比文字，更清楚。 

-1.load
-2.process
-3.show
我觉的这个比较清楚。现出第一个版本。 


## 关于 Python 解释器运行的问题。。
-你在执行`upload_new_version.sh`脚本时遇到了一个`SyntaxError: invalid syntax`错误，这个错误是在执行`renew_setup_version.py`脚本时产生的。出错的代码是一个`print`函数调用，这个函数调用使用了Python 3.6引入的f-string语法。

问题是，尽管单独运行`renew_setup_version.py`没有问题，但是当它被bash脚本调用时就会报错。这个问题的原因可能是，你的bash环境使用的Python解释器与你单独运行Python脚本时使用的Python解释器版本不同。可能bash环境使用的是Python 2，而你单独运行脚本时使用的是Python 3。

为了解决这个问题，你可以在bash脚本中明确使用Python 3来执行`renew_setup_version.py`。你可以通过指定Python 3的完整路径或者使用`python3`命令（如果你的环境中已经配置了该命令）。下面是如何修改你的bash脚本：

将

```bash
python ./clear_clean_go_upgrage/renew_setup_version.py
```

修改为

```bash
python3 ./clear_clean_go_upgrage/renew_setup_version.py
```

--修改如下
#!/bin/bash

# Update version number in setup.py
echo "Update version number in setup.py..."
python3 ./clear_clean_go_upgrage/renew_setup_version.py

---

的确，通过脚本 bash  .sh 文件运行时，可能不会理解 别名的问题。因此我们需要修改 .sh文件中的命令。
[Solved! well done]

-- 完成。 

## Task -->在 main.py 的基础上，完成三个部分。或者就是两个部分-读取和分析。
先不想写序号。我觉得序号写得更清楚。 序号比文字，更清楚。 

-1.load
-2.process
-3.show
我觉的这个比较清楚。现出第一个版本。 
-

----很好！ 先本地测试： python main. 
之后完成 uplaoad...
then ,在 tests 测试， test_m1m2m3.py
----
完成测试。
pytest -s test_pytest_m1m2m3.py

------
20230627-先后有一个基本的框架-有一个基本的思路。 
-1. 看看原来做的是什么？


demand_forcast_retail:
python yourge_data_sales_supply_inventory.py 
- 以某一种酸奶为例，给出需求，供给，与库存之间的关系。


- data_time_series_v2_Milk_demand_supply.py
比较旧的分析。 需求，供给，库存之间的关系。 

python data_time_series_v2_Milk_product.py
- 只针对牛奶，需求，供给，库存。 


考虑家庭：
-一个简单测试 test_simple_demand.py


python test_extreme_weather.py
-很清楚的展现了极端天气的影响。 


 python data_time_series_v1_10_products.py
 -10种产品的 需求 供给 库存情况

 python read_db_family_data.py
 -早期的程序，对10种食物，三种家庭的需求情况，差异性。 

 -
 website- 其中有一部分更进一步的数据分析


 test_activity_special_date_v2.py
 -经典程序， 可用。 展示了 三种（折扣、节日、极端天气）类别的影响。


python test_activity_sensitivity_weight_1year_v2.py
-随机-四种商品的变化。


app.py 
-柱状图 展示， html  flask 程序来调用 

-------大体回顾了website$ 与demand_forcast_retail 目录下的程序。 

下面看.demand_forcast_retail/release_pypi/kangforecast,这里程序更进一步

-应该是分家庭了。 而且有了普遍的流程。 
kang@Love-Grace kangforecast$ ls -al m*
-rw-r--r--  1 kang  staff    76 Jun 19 13:17 m1load.py
-rw-r--r--  1 kang  staff    64 Jun 19 14:31 m2process.py
-rw-r--r--  1 kang  staff    45 Jun 19 14:40 m3show.py
-rw-r--r--  1 kang  staff  1787 Jun 19 14:41 main.py
-rw-r--r--  1 kang  staff    73 Jun 16 13:40 module1.py
三个module . 
m1
m2 
m3

python main.py 
Starting the process...

m1: Loading data from ../data/testdata.csv...
m1: Data loaded successfully. Type of the data: <class 'pandas.core.frame.DataFrame'> and the data is:
   value
0     10
1     20
2     30
3     40
4     50

m2: Processing data...
m2: Data processing complete. Type of the processed data: <class 'numpy.float64'> and the data is:
30.0

m3: Displaying processed data...
30.0
m3: Data displayed successfully.

Process complete!
---


# In main.py
from kangforecast.m1load import m1load
from kangforecast.m2process import m2process
from kangforecast.m3show import m3show

def main():
    print("Starting the process...\n")

    print("m1: Loading data from ../data/testdata.csv...")
    df = m1load("../data/testdata.csv")
    print(f"m1: Data loaded successfully. Type of the data: {type(df)} and the data is:\n{df}\n")

    print("m2: Processing data...")
    processed_df = m2process(df)
    print(f"m2: Data processing complete. Type of the processed data: {type(processed_df)} and the data is:\n{processed_df}\n")

    print("m3: Displaying processed data...")
    m3show(processed_df)
    print("m3: Data displayed successfully.\n")

    print("Process complete!")

if __name__ == "__main__":
    main()
----


-这个框架是很好的。 

看一下 setup.
    entry_points={
        'console_scripts': [
            'kangforecast_command=kangforecast.main:main',
        ],
    },


--
kangforecast$ kangforecast_command
Starting the process...

m1: Loading data from ../data/testdata.csv...
m1: Data loaded successfully. Type of the data: <class 'pandas.core.frame.DataFrame'> and the data is:
   value
0     10
1     20
2     30
3     40
4     50

m2: Processing data...
m2: Data processing complete. Type of the processed data: <class 'numpy.float64'> and the data is:
30.0

m3: Displaying processed data...
30.0
m3: Data displayed successfully.

Process complete!
----


因此，我们目前的情况是  通过 命令行，调取main，并调取main 函数，而后调取  m1 m2 m3. 完成任务。 
----
很好。下面我们执行一个版本自动增加的功能。 

-之前有自动增加的功能，只是通过  .sh 来执行的。  
我们try 下 kangtools

kangtools_upgrade_pypi_package_pip_install -h
usage: kangtools_upgrade_pypi_package_pip_install [-h] package_name

This script performs several steps to update, build, upload and install a new version of a specified Python package. Here are the detailed steps: 1. Updates the version number in the setup.py
file. 2. Removes the old distributions in the 'dist' directory. 3. Builds a new distribution of the package. 4. Uploads the new distribution to PyPI. 5. Uninstalls the old version of the
package. 6. Waits for a while

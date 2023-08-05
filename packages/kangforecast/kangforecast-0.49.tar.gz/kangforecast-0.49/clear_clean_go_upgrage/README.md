确实，你可以在命令行中临时更改你的`PATH`环境变量。首先，你需要知道脚本`clear_clean_go.py`的绝对路径，然后在你的命令行中输入以下命令：

```bash
export PATH=$PATH:/full/path/to/your/clear_clean_go/
```

请将`/full/path/to/your/clear_clean_go/`替换为你的脚本实际的完整路径。你可以使用`pwd`命令来找到当前目录的完整路径。

然后，就像我之前提到的，你需要给你的脚本添加执行权限：

```bash
chmod +x /full/path/to/your/clear_clean_go/clear_clean_go.py
```

并且你需要在你的脚本的顶部添加一个shebang行：

```python
#!/usr/bin/env python3
```

现在你应该可以在任何位置直接运行你的脚本：

```bash
clear_clean_go.py
```

这个`PATH`的更改只在当前的终端会话中有效。如果你关闭并重新打开你的终端，你将需要重新执行这个`export`命令。

这条`export`命令用于在 Unix 和 Unix-like 操作系统（如 Linux 和 macOS）中设置或修改环境变量。

1. `export`是一个 shell 命令，用于将后面定义的变量设置为环境变量，使得该变量在当前 shell 会话和所有从当前会话启动的子会话中可用。
   
2. `PATH`是一个特殊的环境变量，它告诉 shell 在哪些目录下搜索可执行文件。这些目录由冒号 (:) 分隔。

3. `$PATH`是 shell 用来引用环境变量 PATH 的当前值的方式。

4. `:`是一个分隔符，用于在已有的 PATH 值后面添加新的路径。

5. `/full/path/to/your/clear_clean_go/`是你想要添加到 PATH 中的新目录。这应该替换为你的 `clear_clean_go.py` 脚本所在的实际目录。

所以，当你运行这个命令 `export PATH=$PATH:/full/path/to/your/clear_clean_go/` 时，你告诉 shell 把你的 `clear_clean_go.py` 脚本所在的目录添加到 PATH 环境变量中去。这样，你就可以在任何位置运行你的脚本，因为 shell 会在 PATH 中列出的所有目录中查找可执行的脚本和程序。

## ----#  关于版本非最新的情况 
你可以在Python脚本中读取`setup.py`文件的版本号，然后在shell脚本中使用这个版本号来指定安装。以下是一种可能的实现方式：

1. 在`renew_setup_version.py`脚本的最后，将新的版本号写入一个临时文件，如`new_version.txt`：

```python
# 在 renew_setup_version.py 的最后添加以下代码
with open('new_version.txt', 'w') as f:
    f.write(new_version)
```

2. 在你的`upload_new_version.sh`脚本中，读取这个新的版本号，并使用它来指定安装：

```bash
#!/bin/bash

# Update version number in setup.py
echo "Update version number in setup.py..."
python3 ./clear_clean_go_upgrage/renew_setup_version.py

echo "Removing old distributions..."
rm -rf ./dist/*

echo "Building new distribution..."
python setup.py sdist bdist_wheel

echo "Uploading new distribution to PyPI..."
twine upload dist/*

echo "Uninstalling old version of kangforecast..."
pip uninstall -y kangforecast

# Set the waiting time
WAIT_TIME=20

echo "Waiting for the server to update to the latest version...we set 20 seconds. Please take a break or have a cup of coffee."
for ((i=0; i<$WAIT_TIME; i++)); do
  printf "\rWaiting... [%-20s] %d sec" $(printf '%0.s#' $(seq 1 $i)) $i
  sleep 1
done
printf "\n"

echo "Waiting for the server to update to the latest version..."
sleep 20  # waits for 60 seconds. Adjust this value as needed.

# Read the new version number
NEW_VERSION=$(cat new_version.txt)

echo "Installing new version of kangforecast..."
pip install --no-cache-dir kangforecast==$NEW_VERSION

echo "All done!"
```

以上脚本将首先卸载旧版本的`kangforecast`，然后安装你在`setup.py`中指定的新版本。你可以根据你的需求调整这个脚本。
---


-------我们使用休息10秒后，两次安装。 第一次”没有找到“ ，第二次可以安装。应该不是等待时间不够的问题，而是哪里存在一些更新的设置。导致第一次找不到。我们第二次就可以找到，即便时间很短。 

--
您的分析看起来很有道理。这可能是由于PyPI服务器缓存或更新机制导致的。即使在上传后，新版本可能不会立即在所有服务器上可用，可能需要一些时间才能在所有服务器上进行更新和同步。

然而，看起来您的脚本在第二次尝试时能够成功安装新版本，这表明更新和同步确实在您的第一次和第二次尝试之间完成了。这就解释了为什么即使等待时间很短，第二次尝试也可以成功。

如果这种情况频繁发生，您可能希望在您的脚本中添加更多的错误处理和重试逻辑，以便更好地处理这种情况。比如，您可以设置一个循环，如果第一次尝试失败，那么它将等待一个短暂的延迟，然后再试一次，直到成功为止。
---

好的，以下是修改后的脚本：

```bash
#!/bin/bash

# Update version number in setup.py
echo "Update version number in setup.py..."
python3 ./clear_clean_go_upgrage/renew_setup_version.py

echo "Removing old distributions..."
rm -rf ./dist/*

echo "Building new distribution..."
python3 setup.py sdist bdist_wheel

echo "Uploading new distribution to PyPI..."
twine upload dist/*

echo "Uninstalling old version of kangforecast..."
pip3 uninstall -y kangforecast

# Increase the waiting time
WAIT_TIME=10

echo "Waiting for the server to update to the latest version... We set a 10 second break. Grab a cup of coffee and enjoy the view outside."
for ((i=0; i<$WAIT_TIME; i++)); do
  printf "\rWaiting... [%-60s] %d sec" $(printf '%0.s#' $(seq 1 $i)) $i
  sleep 1
done
printf "\n"

# Clear pip cache
echo "Clearing pip cache..."
pip3 cache purge

# Read the new version number
NEW_VERSION=$(cat new_version.txt)

# Try to install new version of kangforecast
max_attempts=3
delay_between_attempts=3

attempt=0
until pip3 install --no-cache-dir kangforecast==$NEW_VERSION
do
    attempt=$((attempt + 1))

    if [ $attempt -ge $max_attempts ]
    then
        echo "尝试次数已达上限。请检查命令或网络状态。"
        exit 1
    fi

    echo "安装失败，等待${delay_between_attempts}秒后进行第${attempt}次尝试...在此期间，您可以喝杯咖啡，欣赏窗外的风景。"
    sleep $delay_between_attempts
done

echo "安装新版本的kangforecast成功！"

echo "All done!"
```
这个脚本会尝试安装新版本的kangforecast，如果失败，将等待一段时间后再次尝试，直到成功或尝试次数达到上限。同时，我也保留了“休息咖啡看风景”的信息。
----

您的分析看起来很有道理。这可能是由于PyPI服务器缓存或更新机制导致的。即使在上传后，新版本可能不会立即在所有服务器上可用，可能需要一些时间才能在所有服务器上进行更新和同步。

然而，看起来您的脚本在第二次尝试时能够成功安装新版本，这表明更新和同步确实在您的第一次和第二次尝试之间完成了。这就解释了为什么即使等待时间很短，第二次尝试也可以成功。

如果这种情况频繁发生，您可能希望在您的脚本中添加更多的错误处理和重试逻辑，以便更好地处理这种情况。比如，您可以设置一个循环，如果第一次尝试失败，那么它将等待一个短暂的延迟，然后再试一次，直到成功为止。
--
”如果这种情况频繁发生，您可能希望在您的脚本中添加更多的错误处理和重试逻辑，以便更好地处理这种情况。比如，您可以设置一个循环，如果第一次尝试失败，那么它将等待一个短暂的延迟，然后再试一次，直到成功为止。“ 这个想法很好。请按照你的思路，完善 sh文件，设置这样一个判断。谢谢！
--好的，以下是一个使用 bash 脚本编写的简单示例。此脚本将尝试运行一个命令，如果命令失败，它将等待一段时间，然后再尝试运行。它将继续这个过程，直到命令成功为止。
--- 解决！
----------

以下是对你提供的三个文件的分析：

1. `clear_clean_go.py` 文件的作用是清理项目的根目录。它删除一些特定类型的文件（例如 .png 和 .log 文件）、删除一些特定名称的目录（例如 `__pycache__`），删除一些特定目录（例如 `dist`）中的内容，以及删除一些特定的目录（例如 `build`, `kangforecast.egg-info`, `env_kangpypi`）。此外，它还可以显示清理前后的目录结构。

2. `renew_setup_version.py` 文件的作用是更新 `setup.py` 文件中的版本号。它会将版本号的最后一个部分（即修订号）加一，然后将新的版本号写回 `setup.py` 文件中。它还会将新的版本号写入到 `new_version.txt` 文件中，供其他脚本或程序使用。

3. `upload_new_version.sh` 是一个 bash 脚本，用于自动化发布新版本的流程。它会调用 `renew_setup_version.py` 更新版本号，然后删除旧的发布包，创建新的发布包，上传新的发布包到 PyPI，卸载旧版本的包，等待一段时间，然后尝试安装新版本的包。如果新版本的包无法成功安装，它会进行多次尝试，每次尝试之间有一定的延迟。

整合这三个文件的一个可能的方案是将 `clear_clean_go.py` 和 `renew_setup_version.py` 合并为一个 Python 脚本，然后在 `upload_new_version.sh` 中调用这个新的 Python 脚本。注意，由于 `upload_new_version.sh` 是一个 bash 脚本，而不是 Python 脚本，所以它的内容不适合直接合并到 Python 脚本中。你可以将它改写为一个 Python 脚本，或者保持它是一个 bash 脚本，然后在其中调用 Python 脚本。
-----


kang@Love-Grace clear_clean_go_upgrage$ ./upload_new_version.sh --help
Usage: ./upload_new_version.sh [options]

Options:
--help                   Display this help message and exit.

This script performs the following steps:
1. Updates version number in setup.py
2. Removes old distributions
3. Builds new distribution
4. Uploads new distribution to PyPI
5. Uninstalls old version of the package
6. Waits for the server to update to the latest version
7. Clears pip cache
8. Tries to install new version of the package

--



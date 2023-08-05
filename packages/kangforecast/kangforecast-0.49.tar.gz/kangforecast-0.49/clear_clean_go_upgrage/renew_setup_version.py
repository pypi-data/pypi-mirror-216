# -*- coding: utf-8 -*-

import re

# 读取 setup.py
with open('setup.py', 'r') as f:
    content = f.read()

# 找到版本号
version_match = re.search(r"version='(.*)'", content)
if version_match is None:
    raise Exception("Could not find version in setup.py")

# 拆分并增加版本号
version_parts = list(map(int, version_match.group(1).split('.')))
version_parts[-1] += 1  # increment the last part of version

# Replace old version with new version
new_version = '.'.join(map(str, version_parts))
# content = re.sub(r"version='(.*)'", f"version='{new_version}'", content)
content = re.sub(r"version='(.*)'", "version='{}'".format(new_version), content)


# 写回 setup.py
with open('setup.py', 'w') as f:
    f.write(content)

print(f'Updated setup.py to version {new_version}')

# 在 renew_setup_version.py 的最后添加以下代码
with open('new_version.txt', 'w') as f:
    f.write(new_version)
#!/usr/bin/env python3
import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 删除自定义标签区域和推荐版块
pattern = r'\s*<!-- 自定义标签区域 -->.*?<!-- 我的推荐版块 -->.*?</div>\s*</div>\s*</div>'
content = re.sub(pattern, '', content, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('已删除自定义关键词区域')

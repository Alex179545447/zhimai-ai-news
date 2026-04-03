#!/usr/bin/env python3
import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 修复热搜榜标题区域 - 找到损坏的部分并替换
old_pattern = r'<span class="section-icon">🔥</span>\s*J条</span>'
new_pattern = '<span class="section-icon">🔥</span>\n                        <span class="section-name">热搜榜</span>\n                        <span class="section-count">10条</span>'
content = re.sub(old_pattern, new_pattern, content)

# 修复热搜列表项格式 - 添加正确的缩进
content = re.sub(
    r'(<div class="hot-item"[^>]*>)\s*<div',
    r'\1\n                            <div',
    content
)

# 更好的方式：直接修复整个hot-list区域
# 查找损坏的热搜标题
if 'J条' in content:
    print("找到损坏的热搜标题，正在修复...")
    content = content.replace('J条</span>', '<span class="section-name">热搜榜</span>\n                        <span class="section-count">10条</span>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("热搜榜标题已修复")

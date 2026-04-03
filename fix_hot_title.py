#!/usr/bin/env python3
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 修复热搜标题
old = '<span class="section-icon">🔥</span>\n                        H条</span>'
new = '<span class="section-icon">🔥</span>\n                        <span class="section-name">热搜榜</span>\n                        <span class="section-count">10条</span>'

content = content.replace(old, new)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("热搜标题已修复")

#!/usr/bin/env python3
import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 查找所有section-header中缺少section-name的位置并修复
# 模式：section-icon后面跟着 H条 或 J条 或其他单字符+条

# 修复热搜榜（已有section-name但缺少）
content = content.replace(
    '<span class="section-icon">🔥</span>\n                        H条</span>',
    '<span class="section-icon">🔥</span>\n                        <span class="section-name">热搜榜</span>\n                        <span class="section-count">10条</span>'
)

# 修复其他section（需要添加section-name）
sections_to_fix = [
    ('🔥', 'AI科技前沿', '4条'),
    ('📈', 'A股与金融市场', '4条'),
    ('🏛️', '政策与宏观', '3条'),
    ('🌍', '国内外热点', '3条'),
]

for icon, name, count in sections_to_fix:
    old = f'<span class="section-icon">{icon}</span>\n                        H条</span>'
    new = f'<span class="section-icon">{icon}</span>\n                        <span class="section-name">{name}</span>\n                        <span class="section-count">{count}</span>'
    content = content.replace(old, new)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("所有section标题已修复")

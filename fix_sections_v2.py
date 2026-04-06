#!/usr/bin/env python3
import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 修复所有section的section-count标签
sections = [
    ('🤖', 'AI与科技前沿', '4条'),
    ('📈', 'A股与金融市场', '4条'),
    ('🏛️', '政策与宏观', '3条'),
    ('🌍', '国际热点', '3条'),
    ('🔥', '热搜榜', '10条'),
]

for icon, name, count in sections:
    # 匹配损坏的结构：section-name后面直接跟 H条 或 J条
    pattern = r'(<span class="section-icon">%s</span>\s*<span class="section-name">%s</span>\s*)%s</span>' % (icon, name, r'[HJ]条')
    replacement = r'\1<span class="section-count">%s</span>' % count
    content = re.sub(pattern, replacement, content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("所有section-count已修复")

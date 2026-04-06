#!/usr/bin/env python3
"""一次性彻底修复GitHub HTML中的所有问题"""
import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 修复所有section的section-count标签
fixes = [
    ('🤖', 'AI与科技前沿', '4条'),
    ('📈', 'A股与金融市场', '4条'),
    ('🏛️', '政策与宏观', '3条'),
    ('🌍', '国际热点', '3条'),
    ('🔥', '热搜榜', '10条'),
]
for icon, name, count in fixes:
    # 修复缺少span的结构：J条</span> -> <span class="section-count">X条</span>
    pattern = r'(<span class="section-icon">' + re.escape(icon) + r'</span>\s*<span class="section-name">' + re.escape(name) + r'</span>\s*)J条</span>'
    replacement = r'\1<span class="section-count">' + count + r'</span>'
    content = re.sub(pattern, replacement, content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

# 验证
with open('index.html', 'r', encoding='utf-8') as f:
    check = f.read()

errors = []
if 'J条</span>' in check:
    errors.append("仍有J条")
if 'H条</span>' in check:
    errors.append("仍有H条")

count_spans = check.count('<span class="section-count">')
print(f"section-count数量: {count_spans}")

if errors:
    print("❌ 未修复:", errors)
else:
    print("✅ 所有问题已修复!")

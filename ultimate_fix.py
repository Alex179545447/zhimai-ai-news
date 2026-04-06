#!/usr/bin/env python3
"""彻底一次性修复所有HTML问题"""
import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 修复日期 - 确保有完整的<span>...</span>
content = re.sub(
    r'<span class="date-display"([^>]*)>([^<]*?)(?!</span>)',
    r'<span class="date-display"\1>\2</span>',
    content
)
if 'id="currentDate">' not in content:
    content = re.sub(
        r'<span class="date-display">([^<]*?)</span>',
        r'<span class="date-display" id="currentDate">\1</span>',
        content
    )

# 2. 修复所有section的section-count
fixes = [
    ('🤖', 'AI与科技前沿', '4条'),
    ('📈', 'A股与金融市场', '4条'),
    ('🏛️', '政策与宏观', '3条'),
    ('🌍', '国际热点', '3条'),
    ('🔥', '热搜榜', '10条'),
]
for icon, name, count in fixes:
    # 修复缺少section-count或损坏的结构
    pattern = r'(<span class="section-icon">' + re.escape(icon) + r'</span>\s*<span class="section-name">' + re.escape(name) + r'</span>\s*)J条</span>'
    content = re.sub(pattern, r'\1<span class="section-count">' + count + r'</span>', content)
    pattern2 = r'(<span class="section-icon">' + re.escape(icon) + r'</span>\s*<span class="section-name">' + re.escape(name) + r'</span>\s*)</div>'
    content = re.sub(pattern2, r'\1<span class="section-count">' + count + r'</span></div>', content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

# 验证
with open('index.html', 'r', encoding='utf-8') as f:
    check = f.read()

errors = []
if 'J条' in check or 'H条' in check:
    errors.append("仍有J条/H条")
if 'id="currentDate">' not in check:
    errors.append("currentDate缺失")
if 'section-count">' not in check:
    errors.append("section-count缺失")

if errors:
    print("❌ 未修复:", errors)
else:
    print("✅ 所有问题已修复!")

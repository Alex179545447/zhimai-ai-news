#!/usr/bin/env python3
"""彻底修复HTML中的所有问题"""
import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 修复日期显示
content = re.sub(r'<span class="date-display"[^>]*>[^<]*</span>', 
                 '<span class="date-display" id="currentDate">2026年4月6日 · 星期日</span>', content)
if 'id="currentDate"' not in content:
    content = content.replace('<span class="date-display" id="currentDate">2026年4月6日 · 星期日', 
                             '<span class="date-display" id="currentDate">2026年4月6日 · 星期日</span>')

# 2. 修复所有section的section-count
fixes = [
    ('🤖', 'AI与科技前沿', '4条'),
    ('📈', 'A股与金融市场', '4条'),
    ('🏛️', '政策与宏观', '3条'),
    ('🌍', '国际热点', '3条'),
    ('🔥', '热搜榜', '10条'),
]
for icon, name, count in fixes:
    # 修复缺少section-count的结构
    pattern = r'(<span class="section-icon">' + re.escape(icon) + r'</span>\s*<span class="section-name">' + re.escape(name) + r'</span>\s*)J条</span>'
    replacement = r'\1<span class="section-count">' + count + r'</span>'
    content = re.sub(pattern, replacement, content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ HTML彻底修复完成")

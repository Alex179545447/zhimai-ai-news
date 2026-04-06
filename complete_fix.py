#!/usr/bin/env python3
"""一次性彻底修复所有HTML问题"""
import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 修复所有section的section-count标签
fixes = [
    # (图标, 名称, 数量)
    ('🤖', 'AI与科技前沿', '4条'),
    ('📈', 'A股与金融市场', '4条'),
    ('🏛️', '政策与宏观', '3条'),
    ('🌍', '国际热点', '3条'),
    ('🔥', '热搜榜', '10条'),
]

for icon, name, count in fixes:
    # 修复损坏的结构：section-name后面跟着 J条 或 H条
    pattern = r'(<span class="section-icon">' + re.escape(icon) + r'</span>\s*<span class="section-name">' + re.escape(name) + r'</span>\s*)[HJ]条</span>'
    replacement = r'\1<span class="section-count">' + count + r'</span>'
    content = re.sub(pattern, replacement, content)
    
    # 也修复没有section-name的结构
    pattern2 = r'(<span class="section-icon">' + re.escape(icon) + r'</span>\s*)J条</span>'
    replacement2 = r'\1<span class="section-name">' + name + r'</span>\n                        <span class="section-count">' + count + r'</span>'
    content = re.sub(pattern2, replacement2, content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

# 验证修复
with open('index.html', 'r', encoding='utf-8') as f:
    check = f.read()
    
if 'J条' in check or 'H条' in check:
    print("❌ 仍有未修复的J条/H条")
else:
    print("✅ 所有section-count标签已修复")

# 检查section-name是否存在
for icon, name, _ in fixes:
    if f'<span class="section-name">{name}</span>' not in check:
        print(f"❌ {name} 的section-name缺失")
    else:
        print(f"✅ {name} 的section-name存在")

#!/usr/bin/env python3
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 修复日期 - 确保有</span>
import re
content = re.sub(r'(id="currentDate">[^<]+)</span>', r'\1</span>', content)
content = re.sub(r'(id="currentDate">[^<]+)(?!</span>)', r'\1</span>', content)

# 修复热搜榜section-count
content = re.sub(
    r'(<span class="section-icon">🔥</span>\s*<span class="section-name">热搜榜</span>\s*)J条</span>',
    r'\1<span class="section-count">10条</span>',
    content
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ 最终修复完成")

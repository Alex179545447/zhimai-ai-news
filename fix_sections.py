#!/usr/bin/env python3

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 修复所有被污染的 section-count（H条 -> 正确数字）
# 热搜榜
content = content.replace(
    '<span class="section-icon">🔥</span>\n                        <span class="section-name">热搜榜</span>\n                        H条</span>',
    '<span class="section-icon">🔥</span>\n                        <span class="section-name">热搜榜</span>\n                        <span class="section-count">10条</span>'
)

# AI科技前沿
content = content.replace(
    '<span class="section-icon">🤖</span>\n                        <span class="section-name">AI与科技前沿</span>\n                        H条</span>',
    '<span class="section-icon">🤖</span>\n                        <span class="section-name">AI与科技前沿</span>\n                        <span class="section-count">4条</span>'
)

# A股与金融市场
content = content.replace(
    '<span class="section-icon">📈</span>\n                        <span class="section-name">A股与金融市场</span>\n                        H条</span>',
    '<span class="section-icon">📈</span>\n                        <span class="section-name">A股与金融市场</span>\n                        <span class="section-count">4条</span>'
)

# 政策与宏观
content = content.replace(
    '<span class="section-icon">🏛️</span>\n                        <span class="section-name">政策与宏观</span>\n                        H条</span>',
    '<span class="section-icon">🏛️</span>\n                        <span class="section-name">政策与宏观</span>\n                        <span class="section-count">3条</span>'
)

# 国际热点
content = content.replace(
    '<span class="section-icon">🌍</span>\n                        <span class="section-name">国际热点</span>\n                        H条</span>',
    '<span class="section-icon">🌍</span>\n                        <span class="section-name">国际热点</span>\n                        <span class="section-count">3条</span>'
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Section标题修复完成")

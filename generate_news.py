#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智脉AI每日早报 - 智能新闻更新脚本
功能：使用智谱GLM-4联网搜索获取最新新闻，自动更新网页内容
"""
import os
import re
import json
import requests
from datetime import datetime

# 智谱API配置
API_KEY = "28133690e57f4ba9902b4015f21404bb.L3eQw0LRHCFM7N9f"
API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

# 自定义标签配置
DEFAULT_CUSTOM_TAGS = [
    "新能源汽车", "锂电池", "光伏太阳能", "储能技术",
    "医药生物", "创新药", "医疗器械", "半导体芯片",
    "人工智能", "大模型", "机器人", "元宇宙",
    "房地产", "消费电子", "电商直播", "游戏版号",
    "国企改革", "数字经济", "碳中和", "稀土资源"
]

def load_custom_tags():
    """从文件加载自定义标签"""
    tags_file = 'custom_tags.txt'
    if os.path.exists(tags_file):
        try:
            with open(tags_file, 'r', encoding='utf-8') as f:
                tags = [line.strip() for line in f if line.strip()]
            if tags:
                return tags
        except:
            pass
    return DEFAULT_CUSTOM_TAGS

def generate_news_prompt():
    """生成新闻获取提示词"""
    tags = load_custom_tags()
    tags_str = '、'.join(tags[:15])
    today = datetime.now()
    date_str = today.strftime('%Y年%m月%d日')
    
    return f"""请搜索今天({date_str})的最新财经新闻，要求：
1. 只搜索最近24小时内的新闻
2. 按以下类别返回JSON格式：

返回格式（只返回JSON，不要其他内容）：
{{
  "date": "{today.strftime('%Y-%m-%d')}",
  "marketTitle": "今日市场基调一句话",
  "marketDesc": "市场基调详细说明",
  "ai": [
    {{"id": "ai-1", "title": "标题", "date": "YYYY-MM-DD HH:MM", "source": "来源", "desc": "摘要", "url": "链接", "tag": "fact|expect", "tagText": "标签文字"}}
  ],
  "market": [
    {{"id": "market-1", "title": "标题", "date": "YYYY-MM-DD", "source": "来源", "desc": "摘要", "url": "链接", "tag": "fact|expect"}}
  ],
  "policy": [
    {{"id": "policy-1", "title": "标题", "date": "YYYY-MM-DD", "source": "来源", "desc": "摘要", "url": "链接"}}
  ],
  "global": [
    {{"id": "global-1", "title": "标题", "date": "YYYY-MM-DD", "source": "来源", "desc": "摘要", "url": "链接"}}
  ],
  "hot": ["热搜1", "热搜2", "热搜3", "热搜4", "热搜5"],
  "table": [
    {{"event": "事件", "sectors": ["板块1", "板块2"], "logic": "影响逻辑", "url": "链接"}}
  ],
  "custom": [
    {{"title": "标题", "date": "YYYY-MM-DD", "source": "来源", "desc": "摘要", "url": "链接", "tag": "标签"}}
  ]
}}"""

def get_news_from_glm(prompt):
    """调用智谱GLM-4 API获取新闻"""
    try:
        response = requests.post(
            API_URL,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "glm-4-flash",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "tools": [
                    {
                        "type": "web_search",
                        "web_search": {"search_engine": "bing"}
                    }
                ],
                "stream": False
            },
            timeout=180
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            return content
        else:
            print(f"API错误: {response.status_code}")
            return None
    except Exception as e:
        print(f"请求失败: {e}")
        return None

def extract_json_from_response(content):
    """从API响应中提取JSON"""
    match = re.search(r'```json\s*([\s\S]*?)\s*```', content)
    if match:
        return match.group(1)
    match = re.search(r'\{[\s\S]*\}', content)
    if match:
        return match.group(0)
    return None

def update_html_file(news_data):
    """更新HTML文件"""
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        today = datetime.now()
        date_str = today.strftime('%Y年%m月%d日')
        weekdays = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六']
        weekday = weekdays[today.weekday()]
        full_date = f"{date_str} · {weekday}"
        
        # 更新日期
        pattern = r'id="currentDate">[^<]+'
        replacement = f'id="currentDate">{full_date}'
        content = re.sub(pattern, replacement, content)
        
        # 更新市场基调标题
        if 'marketTitle' in news_data:
            pattern = r'<div class="market-title">[^<]+'
            content = re.sub(pattern, f'<div class="market-title">{news_data["marketTitle"]}', content)
        
        # 更新市场基调描述
        if 'marketDesc' in news_data:
            pattern = r'<div class="market-desc">[\s\S]*?</div>\s*</div>\s*</div>\s*<!-- 标签栏 -->'
            match = re.search(pattern, content)
            if match:
                new_desc = f'''<div class="market-desc">
                {news_data["marketDesc"]}
            </div>
        </div>

        <!-- 标签栏 -->'''
                content = content.replace(match.group(0), new_desc)
        
        # 更新新闻日期
        news_date = news_data.get('date', today.strftime('%Y-%m-%d'))
        content = re.sub(r'(\d{{4}}-\d{{2}}-\d{{2}})\s*<!-- AI与科技前沿 -->', 
                        f'{news_date}<!-- AI与科技前沿 -->', content)
        
        # 更新fullNewsData中的日期
        content = re.sub(r"date: '(\d{4}-\d{2}-\d{2})", f"date: '{news_date}", content)
        
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ HTML已更新: {full_date}")
        return True
    except Exception as e:
        print(f"❌ 更新HTML失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 50)
    print("智脉AI每日早报 - 智能新闻更新任务")
    print("=" * 50)
    print(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)
    
    # 获取新闻
    print("📡 正在调用智谱GLM-4获取最新新闻...")
    prompt = generate_news_prompt()
    news_content = get_news_from_glm(prompt)
    
    if news_content:
        print("✅ 成功获取新闻内容")
        print("-" * 50)
        
        # 保存原始内容
        with open('news_raw.txt', 'w', encoding='utf-8') as f:
            f.write(news_content)
        print("📄 原始内容已保存到 news_raw.txt")
        
        # 解析JSON
        json_str = extract_json_from_response(news_content)
        
        if json_str:
            try:
                news_data = json.loads(json_str)
                print(f"✅ 解析JSON成功")
                print(f"   AI新闻: {len(news_data.get('ai', []))}条")
                print(f"   市场新闻: {len(news_data.get('market', []))}条")
                print(f"   政策新闻: {len(news_data.get('policy', []))}条")
                print(f"   全球新闻: {len(news_data.get('global', []))}条")
                print(f"   热搜: {len(news_data.get('hot', []))}条")
                
                # 更新HTML
                if update_html_file(news_data):
                    print("-" * 50)
                    print("✅ 更新完成!")
                    return True
            except json.JSONDecodeError as e:
                print(f"❌ JSON解析失败: {e}")
        else:
            print("❌ 未找到JSON数据")
    else:
        print("❌ 获取新闻失败")
    
    return False

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)

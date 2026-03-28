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

def get_news_from_glm(prompt):
    """调用智谱GLM-4 API获取新闻"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "glm-4-flash",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "tools": [
            {
                "type": "web_search",
                "web_search": {
                    "search_engine": "bing"
                }
            }
        ],
        "stream": False
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=data, timeout=120)
        if response.status_code == 200:
            result = response.json()
            return result.get("choices", [{}])[0].get("message", {}).get("content", "")
        else:
            print(f"API错误: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"请求失败: {e}")
        return None

def generate_news_prompt():
    """生成获取新闻的提示词"""
    today = datetime.now()
    date_str = today.strftime('%Y年%m月%d日')
    weekdays = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六']
    weekday = weekdays[today.weekday()]
    
    return f"""请搜索今天({date_str} {weekday})的最新新闻，生成一份每日早报。

要求：
1. 只搜索最近24小时内的新闻
2. 按以下5个类别整理，返回JSON数组格式：

【类别1：AI与科技前沿】
- AI行业动态、大模型进展、机器人、半导体、算力、科技巨头动向

【类别2：A股与金融市场】  
- A股行情、板块热点、基金市场、融资并购、金融监管、宏观经济数据
- 区分"已落地事实"与"市场预期/传闻"

【类别3：北京政策与宏观风向】
- 国家层面新政、国务院/部委重要会议、证监会/央行发声

【类别4：职场动态】
- 就业市场、招聘动态、职场趋势

【类别5：国内外其他热点】
- 国际地缘政治、国外新政、海外市场、社会热点

请按以下JSON格式返回（只返回JSON，不要其他内容）：
{{
  "market": "今日市场基调的一句话总结",
  "ai": [{{"title": "新闻标题", "date": "日期", "source": "来源", "desc": "摘要50字内", "url": "链接", "tag": "fact|expect"}}],
  "market": [{{"title": "新闻标题", "date": "日期", "source": "来源", "desc": "摘要", "url": "链接", "tag": "fact|expect"}}],
  "policy": [{{"title": "新闻标题", "date": "日期", "source": "来源", "desc": "摘要", "url": "链接", "tag": "policy"}}],
  "career": [{{"title": "新闻标题", "date": "日期", "source": "来源", "desc": "摘要", "url": "链接"}}],
  "global": [{{"title": "新闻标题", "date": "日期", "source": "来源", "desc": "摘要", "url": "链接"}}],
  "table": [{{"event": "事件", "sectors": ["板块1", "板块2"], "logic": "影响逻辑", "url": "链接"}}]
}}"""

def extract_json_from_response(content):
    """从API响应中提取JSON"""
    # 尝试提取JSON代码块
    match = re.search(r'```json\s*([\s\S]*?)\s*```', content)
    if match:
        return match.group(1)
    
    # 尝试提取普通JSON
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
        
        # 更新市场基调
        if 'market_summary' in news_data:
            pattern = r'<div class="market-summary">[\s\S]*?<p>[^<]*</p>'
            match = re.search(pattern, content)
            if match:
                content = content.replace(
                    match.group(0),
                    f'<div class="market-summary">\n            <h2>📊 今日市场基调</h2>\n            <p>{news_data["market_summary"]}</p>'
                )
        
        # 更新新闻数据
        news_json = json.dumps(news_data, ensure_ascii=False, indent=2)
        
        # 替换 newsData 对象
        pattern = r'var newsData = \{[\s\S]*?\};'
        replacement = f'var newsData = {news_json};'
        content = re.sub(pattern, replacement, content)
        
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
                print(f"   职场新闻: {len(news_data.get('career', []))}条")
                print(f"   全球新闻: {len(news_data.get('global', []))}条")
                print(f"   表格数据: {len(news_data.get('table', []))}条")
                
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

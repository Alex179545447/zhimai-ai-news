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
API_KEY = os.environ.get("ZHIPU_API_KEY", "28133690e57f4ba9902b4015f21404bb.L3eQw0LRHCFM7N9f")
API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"


def get_news_from_glm():
    """调用智谱GLM-4 API获取新闻"""
    today = datetime.now()
    date_str = today.strftime('%Y年%m月%d日')
    
    prompt = f"""请搜索今天({date_str})的最新财经新闻，要求：
1. 只搜索最近24小时内的新闻
2. 按以下JSON格式返回，包含完整的新闻内容：

{{
  "date": "{today.strftime('%Y-%m-%d')}",
  "weekday": "{['星期日','星期一','星期二','星期三','星期四','星期五','星期六'][today.weekday()]}",
  "marketTitle": "今日市场基调一句话(不超过15字)",
  "marketDesc": "市场基调详细说明(50字以内)",
  "ai": [
    {{"title": "新闻标题1", "date": "{today.strftime('%Y-%m-%d')}", "source": "来源", "desc": "摘要简述", "tag": "🔥重磅"}},
    {{"title": "新闻标题2", "date": "{today.strftime('%Y-%m-%d')}", "source": "来源", "desc": "摘要简述", "tag": "AI"}},
    {{"title": "新闻标题3", "date": "{today.strftime('%Y-%m-%d')}", "source": "来源", "desc": "摘要简述", "tag": "科技"}}
  ],
  "market": [
    {{"title": "新闻标题1", "date": "{today.strftime('%Y-%m-%d')}", "source": "来源", "desc": "摘要简述", "tag": "✅已落地"}},
    {{"title": "新闻标题2", "date": "{today.strftime('%Y-%m-%d')}", "source": "来源", "desc": "摘要简述", "tag": "市场"}},
    {{"title": "新闻标题3", "date": "{today.strftime('%Y-%m-%d')}", "source": "来源", "desc": "摘要简述", "tag": "板块"}}
  ],
  "policy": [
    {{"title": "新闻标题1", "date": "{today.strftime('%Y-%m-%d')}", "source": "来源", "desc": "摘要简述", "tag": "📋政策"}},
    {{"title": "新闻标题2", "date": "{today.strftime('%Y-%m-%d')}", "source": "来源", "desc": "摘要简述", "tag": "宏观"}}
  ],
  "global": [
    {{"title": "新闻标题1", "date": "{today.strftime('%Y-%m-%d')}", "source": "来源", "desc": "摘要简述", "tag": "🔥地缘"}},
    {{"title": "新闻标题2", "date": "{today.strftime('%Y-%m-%d')}", "source": "来源", "desc": "摘要简述", "tag": "国际"}},
    {{"title": "新闻标题3", "date": "{today.strftime('%Y-%m-%d')}", "source": "来源", "desc": "摘要简述", "tag": "大宗"}}
  ],
  "hot": ["热搜1", "热搜2", "热搜3", "热搜4", "热搜5", "热搜6", "热搜7", "热搜8", "热搜9", "热搜10"],
  "table": [
    {{"event": "事件1", "sector": "板块", "logic": "影响逻辑"}},
    {{"event": "事件2", "sector": "板块", "logic": "影响逻辑"}},
    {{"event": "事件3", "sector": "板块", "logic": "影响逻辑"}},
    {{"event": "事件4", "sector": "板块", "logic": "影响逻辑"}}
  ]
}}

只返回JSON，不要其他内容。
"""

    try:
        response = requests.post(
            API_URL,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "glm-4-flash",
                "messages": [{"role": "user", "content": prompt}],
                "tools": [{"type": "web_search", "web_search": {"search_engine": "bing"}}],
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


def extract_json(content):
    """提取JSON"""
    match = re.search(r'```json\s*([\s\S]*?)\s*```', content)
    if match:
        return match.group(1)
    match = re.search(r'\{[\s\S]*\}', content)
    if match:
        return match.group(0)
    return None


def escape_js(text):
    """转义JavaScript字符串"""
    if not text:
        return ""
    return text.replace('\\', '\\\\').replace('"', '\\"').replace("'", "\\'").replace('\n', '\\n').replace('\r', '')


def update_html(news_data):
    """更新HTML文件"""
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    today = news_data.get('date', datetime.now().strftime('%Y-%m-%d'))
    weekday = news_data.get('weekday', '')
    full_date = f"{today[:4]}年{int(today[5:7])}月{int(today[8:10])}日 · {weekday}"
    
    # 更新日期
    content = re.sub(r'id="currentDate">[^<]+', f'id="currentDate">{full_date}', content)
    
    # 更新市场基调
    if 'marketTitle' in news_data:
        content = re.sub(r'市场基调：[^<]+', f"市场基调：{news_data['marketTitle']}", content)
    if 'marketDesc' in news_data:
        content = re.sub(r'美伊局势升温[^<]+', news_data.get('marketDesc', ''), content)
    
    # 更新新闻日期
    content = re.sub(r'\d{4}-\d{2}-\d{2}(?=#_#)', today, content)
    
    # 更新fullNewsData
    news_json = json.dumps(news_data, ensure_ascii=False)
    content = re.sub(
        r'var fullNewsData = \{[^}]+\}',
        f'var fullNewsData = {news_json}',
        content
    )
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ HTML已更新: {full_date}")
    return True


def main():
    print("=" * 50)
    print("智脉AI每日早报 - 智能新闻更新任务")
    print("=" * 50)
    print(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)
    
    print("📡 正在调用智谱GLM-4获取最新新闻...")
    news_content = get_news_from_glm()
    
    if news_content:
        print("✅ 成功获取新闻内容")
        
        json_str = extract_json(news_content)
        if json_str:
            try:
                news_data = json.loads(json_str)
                print(f"✅ 解析JSON成功")
                print(f"   AI新闻: {len(news_data.get('ai', []))}条")
                print(f"   市场新闻: {len(news_data.get('market', []))}条")
                print(f"   政策新闻: {len(news_data.get('policy', []))}条")
                print(f"   全球新闻: {len(news_data.get('global', []))}条")
                
                if update_html(news_data):
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

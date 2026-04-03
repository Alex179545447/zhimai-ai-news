#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智脉AI每日晚报 - 智能新闻更新脚本 V2
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

def test_network():
    """测试网络连接"""
    print("🔍 测试网络连接...")
    try:
        response = requests.get("https://open.bigmodel.cn", timeout=10)
        print(f"   ✅ 网络正常 - 状态码: {response.status_code}")
        return True
    except Exception as e:
        print(f"   ❌ 网络连接失败: {e}")
        return False

def get_news_from_glm():
    """调用智谱GLM-4 API获取新闻"""
    today = datetime.now()
    date_str = today.strftime('%Y年%m月%d日')
    date_iso = today.strftime('%Y-%m-%d')
    yesterday = (today.replace(hour=0, minute=0, second=0)).strftime('%Y-%m-%d')
    weekday = ['星期日','星期一','星期二','星期三','星期四','星期五','星期六'][today.weekday()]
    
    prompt = f"""重要提示：今天是{date_str}（{weekday}）。请务必搜索{date_str}当天的最新新闻！

请用必应搜索"{date_str} 最新财经新闻 {date_str} 最新科技新闻 {date_str} A股行情"，

然后按以下JSON格式返回今天的新闻（每条新闻的date字段必须全部是：{date_iso}）：

{{
  "date": "{date_iso}",
  "weekday": "{weekday}",
  "marketTitle": "一句话总结今日市场核心情绪(不超过15字)",
  "marketDesc": "详细说明市场整体表现和关键数据(60字以内)",
  "ai": [
    {{
      "title": "【AI科技】具体新闻标题，包含公司名或技术名",
      "date": "{date_iso}",
      "source": "权威媒体名称",
      "desc": "详细描述：包含具体数据、百分比、金额等。",
      "tag": "AI芯片"
    }},
    {{
      "title": "【AI科技】具体新闻标题",
      "date": "{date_iso}",
      "source": "权威媒体名称",
      "desc": "详细描述：包含具体数据。",
      "tag": "大模型"
    }},
    {{
      "title": "【AI科技】具体新闻标题",
      "date": "{date_iso}",
      "source": "权威媒体名称",
      "desc": "详细描述：包含具体数据。",
      "tag": "机器人"
    }},
    {{
      "title": "【AI科技】具体新闻标题",
      "date": "{date_iso}",
      "source": "权威媒体名称",
      "desc": "详细描述：包含具体数据。",
      "tag": "科技巨头"
    }}
  ],
  "market": [
    {{
      "title": "【A股】具体新闻标题，包含板块名",
      "date": "{date_iso}",
      "source": "权威媒体名称",
      "desc": "详细描述：包含具体涨跌幅、市值等。",
      "tag": "✅已落地"
    }},
    {{
      "title": "【A股】具体新闻标题",
      "date": "{date_iso}",
      "source": "权威媒体名称",
      "desc": "详细描述：包含具体数据。",
      "tag": "板块"
    }},
    {{
      "title": "【A股】具体新闻标题",
      "date": "{date_iso}",
      "source": "权威媒体名称",
      "desc": "详细描述：包含具体数据。",
      "tag": "大盘"
    }},
    {{
      "title": "【基金/北向】具体新闻标题",
      "date": "{date_iso}",
      "source": "权威媒体名称",
      "desc": "详细描述：包含具体资金数据。",
      "tag": "资金"
    }}
  ],
  "policy": [
    {{
      "title": "【政策】具体政策标题，包含出台部门",
      "date": "{date_iso}",
      "source": "新华社/中国政府网/证监会官网",
      "desc": "详细描述：政策核心内容。",
      "tag": "📋国务院"
    }},
    {{
      "title": "【监管】具体监管动态",
      "date": "{date_iso}",
      "source": "证监会/央行官网",
      "desc": "详细描述：监管措施。",
      "tag": "📋证监会"
    }},
    {{
      "title": "【数据】宏观经济数据发布",
      "date": "{date_iso}",
      "source": "国家统计局",
      "desc": "详细描述：具体数据数值。",
      "tag": "📋宏观"
    }}
  ],
  "global": [
    {{
      "title": "【国际】具体国际新闻，包含国家或地区",
      "date": "{date_iso}",
      "source": "路透社/彭博社",
      "desc": "详细描述：事件核心。",
      "tag": "🔥地缘"
    }},
    {{
      "title": "【国际】具体国际新闻",
      "date": "{date_iso}",
      "source": "路透社/彭博社",
      "desc": "详细描述：事件核心内容。",
      "tag": "🇺🇸美股"
    }},
    {{
      "title": "【国际】具体国际新闻",
      "date": "{date_iso}",
      "source": "路透社/彭博社",
      "desc": "详细描述：大宗商品或汇率。",
      "tag": "📊大宗"
    }}
  ],
  "hot": [
    "热搜话题1",
    "热搜话题2",
    "热搜话题3",
    "热搜话题4",
    "热搜话题5",
    "热搜话题6",
    "热搜话题7",
    "热搜话题8",
    "热搜话题9",
    "热搜话题10",
    "热搜话题11",
    "热搜话题12"
  ],
  "table": [
    {{
      "event": "具体事件名称",
      "sector": "影响板块",
      "logic": "影响逻辑"
    }},
    {{
      "event": "具体事件名称",
      "sector": "影响板块",
      "logic": "影响逻辑"
    }},
    {{
      "event": "具体事件名称",
      "sector": "影响板块",
      "logic": "影响逻辑"
    }},
    {{
      "event": "具体事件名称",
      "sector": "影响板块",
      "logic": "影响逻辑"
    }},
    {{
      "event": "具体事件名称",
      "sector": "影响板块",
      "logic": "影响逻辑"
    }}
  ]
}}

重要要求：
1. 所有新闻必须是{date_str}当天的真实事件，date字段必须全部是{date_iso}
2. 描述必须包含具体数字、数据、百分比
3. 只返回JSON，不要任何其他文字
"""

    print(f"📡 开始调用智谱API...")
    print(f"   今天日期: {date_str}")
    print(f"   ISO日期: {date_iso}")
    print(f"   请求超时: 300秒")
    
    try:
        print("⏳ 发送请求中...")
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
            timeout=300
        )
        
        print(f"📥 收到响应 - 状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            print(f"✅ API调用成功，内容长度: {len(content)} 字符")
            return content
        else:
            print(f"❌ API错误: {response.status_code}")
            print(f"   响应内容: {response.text[:500]}")
            return None
            
    except requests.exceptions.Timeout:
        print("❌ 请求超时 (300秒)")
        return None
    except requests.exceptions.ConnectionError as e:
        print(f"❌ 连接错误: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求异常: {e}")
        return None
    except Exception as e:
        print(f"❌ 未知错误: {e}")
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


def build_news_item(news, category):
    """构建新闻条目"""
    title = news.get('title', '')
    date = news.get('date', '')
    source = news.get('source', '')
    desc = news.get('desc', '')
    tag = news.get('tag', '')
    news_id = news.get('id', f'{category}-{hash(title) % 1000}')
    
    return f"""            '{news_id}': {{
                title: '{title.replace("'", "\\'")}',
                tags: [{{ text: '{tag}', class: '' }}],
                source: '{source}',
                url: '#',
                date: '{date}',
                content: `<p><strong>【摘要】</strong>{desc}</p>`,
                relatedTags: [],
                aiInsight: `<p>详见相关新闻</p>`,
                relatedNews: []
            }}"""


def build_hot_item(title, rank, category='hot'):
    """构建热搜条目"""
    news_id = f'{category}-{rank}'
    return f"""            '{news_id}': {{ title: '{title.replace("'", "\\'")}', tags: [{{ text: '热', class: '' }}], source: '热搜', url: '#', date: '{datetime.now().strftime('%Y-%m-%d')}', content: '<p>详见：<a href="#">{title}</a></p>', relatedTags: [], aiInsight: '<p>热搜话题</p>', relatedNews: [] }}"""


def update_html(news_data):
    """更新HTML文件"""
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    today = news_data.get('date', datetime.now().strftime('%Y-%m-%d'))
    weekday = news_data.get('weekday', '')
    full_date = f"{today[:4]}年{int(today[5:7])}月{int(today[8:10])}日 · {weekday}"
    
    # 1. 更新日期显示
    content = re.sub(r'id="currentDate">[^<]+', f'id="currentDate">{full_date}', content)
    
    # 2. 更新市场基调
    if 'marketTitle' in news_data:
        content = re.sub(r'市场基调：[^<]+', f"市场基调：{news_data['marketTitle']}", content)
    if 'marketDesc' in news_data:
        content = re.sub(r'美伊局势升温[^<]+', news_data.get('marketDesc', ''), content)
    
    # 3. 构建新的新闻数据
    news_items = []
    
    # AI新闻 - 4条
    for i, news in enumerate(news_data.get('ai', []), 1):
        news['id'] = f'ai-{i}'
        news_items.append(build_news_item(news, 'ai'))
    
    # 市场新闻 - 4条
    for i, news in enumerate(news_data.get('market', []), 1):
        news['id'] = f'stock-{i}'
        news_items.append(build_news_item(news, 'stock'))
    
    # 政策新闻 - 3条
    for i, news in enumerate(news_data.get('policy', []), 1):
        news['id'] = f'policy-{i}'
        news_items.append(build_news_item(news, 'policy'))
    
    # 国际新闻 - 3条
    for i, news in enumerate(news_data.get('global', []), 1):
        news['id'] = f'global-{i}'
        news_items.append(build_news_item(news, 'global'))
    
    # 热搜 - 12条
    for i, title in enumerate(news_data.get('hot', []), 1):
        news_items.append(build_hot_item(title, i))
    
    # 4. 替换新闻数据
    new_data_block = "        const fullNewsData = {\n" + ",\n".join(news_items) + "\n        };"
    
    # 使用标记替换
    start_marker = '// NEWS_DATA_START'
    end_marker = '// NEWS_DATA_END'
    
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)
    
    if start_idx != -1 and end_idx != -1:
        new_content = content[:start_idx] + start_marker + '\n' + new_data_block + '\n' + end_marker + content[end_idx + len(end_marker):]
    else:
        print("❌ 未找到新闻数据标记")
        return False
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ HTML已更新: {full_date}")
    print(f"   🔥 AI科技新闻: {len(news_data.get('ai', []))}条")
    print(f"   📈 A股市场新闻: {len(news_data.get('market', []))}条")
    print(f"   📋 政策动态: {len(news_data.get('policy', []))}条")
    print(f"   🌍 国际热点: {len(news_data.get('global', []))}条")
    print(f"   🔥 热搜榜单: {len(news_data.get('hot', []))}条")
    return True


def main():
    print("=" * 50)
    print("智脉AI每日晚报 V2 - 智能新闻更新任务")
    print("=" * 50)
    print(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)
    
    # 先测试网络
    if not test_network():
        print("❌ 网络测试失败，尝试继续...")
    
    news_content = get_news_from_glm()
    
    if news_content:
        print("✅ 成功获取新闻内容")
        
        json_str = extract_json(news_content)
        if json_str:
            try:
                news_data = json.loads(json_str)
                print("✅ 解析JSON成功")
                
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

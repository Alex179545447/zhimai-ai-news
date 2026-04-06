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
    weekday = ['星期日','星期一','星期二','星期三','星期四','星期五','星期六'][today.weekday()]
    
    prompt = f"""搜索{date_str}的最新财经和科技新闻，返回JSON：
{{
  "date": "{date_iso}",
  "weekday": "{weekday}",
  "marketTitle": "一句话市场情绪(15字内)",
  "marketDesc": "市场表现说明(60字内)",
  "ai": [
    {{"title": "AI科技新闻1", "date": "{date_iso}", "source": "媒体", "desc": "描述", "tag": "AI"}},
    {{"title": "AI科技新闻2", "date": "{date_iso}", "source": "媒体", "desc": "描述", "tag": "芯片"}},
    {{"title": "AI科技新闻3", "date": "{date_iso}", "source": "媒体", "desc": "描述", "tag": "大模型"}},
    {{"title": "AI科技新闻4", "date": "{date_iso}", "source": "媒体", "desc": "描述", "tag": "机器人"}}
  ],
  "market": [
    {{"title": "A股新闻1", "date": "{date_iso}", "source": "媒体", "desc": "描述", "tag": "板块"}},
    {{"title": "A股新闻2", "date": "{date_iso}", "source": "媒体", "desc": "描述", "tag": "大盘"}},
    {{"title": "A股新闻3", "date": "{date_iso}", "source": "媒体", "desc": "描述", "tag": "资金"}},
    {{"title": "A股新闻4", "date": "{date_iso}", "source": "媒体", "desc": "描述", "tag": "基金"}}
  ],
  "policy": [
    {{"title": "政策1", "date": "{date_iso}", "source": "政府网", "desc": "描述", "tag": "国务院"}},
    {{"title": "政策2", "date": "{date_iso}", "source": "证监会", "desc": "描述", "tag": "监管"}},
    {{"title": "政策3", "date": "{date_iso}", "source": "央行", "desc": "描述", "tag": "宏观"}}
  ],
  "global": [
    {{"title": "国际1", "date": "{date_iso}", "source": "路透社", "desc": "描述", "tag": "美股"}},
    {{"title": "国际2", "date": "{date_iso}", "source": "彭博社", "desc": "描述", "tag": "地缘"}},
    {{"title": "国际3", "date": "{date_iso}", "source": "新华社", "desc": "描述", "tag": "大宗"}}
  ],
  "hot": ["热搜1","热搜2","热搜3","热搜4","热搜5","热搜6","热搜7","热搜8","热搜9","热搜10"],
  "table": [
    {{"event": "事件1", "sector": "板块1", "logic": "逻辑1"}},
    {{"event": "事件2", "sector": "板块2", "logic": "逻辑2"}},
    {{"event": "事件3", "sector": "板块3", "logic": "逻辑3"}}
  ]
}}
只返回JSON，不要其他文字。新闻必须是{date_str}的真实事件。"""

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
    # 尝试从代码块中提取
    match = re.search(r'```json\s*([\s\S]*?)\s*```', content)
    if match:
        return match.group(1).strip()
    # 尝试直接匹配JSON对象
    match = re.search(r'\{[\s\S]*\}', content)
    if match:
        json_str = match.group(0)
        # 清理控制字符
        json_str = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', json_str)
        return json_str
    return None


def build_news_item(news, category, today_date):
    """构建新闻条目"""
    title = news.get('title', '').replace("'", "\\'")
    source = news.get('source', '')
    desc = news.get('desc', '')
    tag = news.get('tag', '')
    news_id = news.get('id', f'{category}-{hash(title) % 1000}')
    
    return """            '%s': {
                title: '%s',
                tags: [{ text: '%s', class: '' }],
                source: '%s',
                url: '#',
                date: '%s',
                content: `<p><strong>【摘要】</strong>%s</p>`,
                relatedTags: [],
                aiInsight: `<p>详见相关新闻</p>`,
                relatedNews: []
            }""" % (news_id, title, tag, source, today_date, desc)


def build_hot_item(title, rank, today_date, category='hot'):
    """构建热搜条目"""
    news_id = f'{category}-{rank}'
    title_escaped = title.replace("'", "\\'")
    # 热搜生成简短描述
    hot_desc = "该话题目前位列热搜第%d位，引发广泛讨论。" % rank
    return """            '%s': { title: '%s', tags: [{ text: '热', class: '' }], source: '热搜', url: '#', date: '%s', content: '<p><strong>【热搜话题】</strong>%s</p><p>%s</p>', relatedTags: [], aiInsight: '<p>热搜话题实时更新中</p>', relatedNews: [] }""" % (news_id, title_escaped, today_date, title, hot_desc)


def update_html(news_data):
    """更新HTML文件"""
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 强制使用今天的真实日期，不依赖AI返回的日期
    today_real = datetime.now().strftime('%Y-%m-%d')
    today = news_data.get('date', today_real)
    weekday = news_data.get('weekday', ['星期日','星期一','星期二','星期三','星期四','星期五','星期六'][datetime.now().weekday()])
    
    # 如果AI返回的日期不是今天，强制使用今天日期
    if today != today_real:
        print(f"⚠️ AI返回日期 {today}，强制更新为今天 {today_real}")
        today = today_real
    
    full_date = f"{today[:4]}年{int(today[5:7])}月{int(today[8:10])}日 · {weekday}"
    
    # 1. 更新日期显示
    content = re.sub(r'id="currentDate">[^<]+', f'id="currentDate">{full_date}', content)
    
    # 1.5 更新快速浏览列表中的所有日期
    content = re.sub(r'<span class="news-source">📅 [^<]+</span>', f'<span class="news-source">📅 {today}</span>', content)
    
    # 2. 更新市场基调
    if 'marketTitle' in news_data:
        content = re.sub(r'(今日市场基调：)[^<]+', f"\\1{news_data['marketTitle']}", content)
    if 'marketDesc' in news_data:
        # 匹配market-desc div中的所有内容（到</div>为止）
        pattern = r'(<div class="market-desc">)[^<]*(<)'
        replacement = f'\\1{news_data.get("marketDesc", "")}\\2'
        content = re.sub(pattern, replacement, content)
    
    # 3. 构建新的新闻数据（强制使用今天日期）
    news_items = []
    
    # AI新闻 - 4条
    for i, news in enumerate(news_data.get('ai', []), 1):
        news['id'] = f'ai-{i}'
        news_items.append(build_news_item(news, 'ai', today))
    
    # 市场新闻 - 4条
    for i, news in enumerate(news_data.get('market', []), 1):
        news['id'] = f'stock-{i}'
        news_items.append(build_news_item(news, 'stock', today))
    
    # 政策新闻 - 3条
    for i, news in enumerate(news_data.get('policy', []), 1):
        news['id'] = f'policy-{i}'
        news_items.append(build_news_item(news, 'policy', today))
    
    # 国际新闻 - 3条
    for i, news in enumerate(news_data.get('global', []), 1):
        news['id'] = f'global-{i}'
        news_items.append(build_news_item(news, 'global', today))
    
    # 热搜 - 12条
    for i, title in enumerate(news_data.get('hot', []), 1):
        news_items.append(build_hot_item(title, i, today))
    
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
    
    # 5. 更新热搜榜HTML
    hot_titles = news_data.get('hot', [])[:12]
    if hot_titles:
        hot_items_html = []
        for i, title in enumerate(hot_titles, 1):
            rank_class = f'top{i}' if i <= 3 else ''
            tag = '沸' if i == 1 else ('新' if i <= 3 else '')
            tag_html = f'<span class="hot-tag">{tag}</span>' if tag else ''
            hot_items_html.append(f'''<div class="hot-item" data-news-id="hot-{i}" onclick="openNewsDetail('hot-{i}')">
                            <span class="hot-rank {rank_class}">{i}</span>
                            <span class="hot-title">{title}</span>
                            {tag_html}
                        </div>''')
        
        # 更新热搜榜数量
        hot_count = str(len(hot_titles)) + '条'
        new_content = new_content.replace('<span class="section-count">4条', '<span class="section-count">' + hot_count)
        
        # 替换热搜列表
        hot_list_pattern = r'(<div class="hot-list">)\s*.*?\s*(</div>\s*</div>\s*</div>\s*<!-- 底部总结表格)'
        hot_list_replacement = r'\1\n' + '\n\n'.join(hot_items_html) + r'\n                    \2'
        new_content = re.sub(hot_list_pattern, hot_list_replacement, new_content, flags=re.DOTALL)
    
    # 6. 更新资本市场关键点梳理表格
    keypoints = news_data.get('table', [])
    if keypoints:
        tbody_rows = []
        for item in keypoints:
            event = item.get('event', '')
            sector = item.get('sector', '')
            logic = item.get('logic', '')
            tbody_rows.append(f'''<tr>
                            <td>{event}</td>
                            <td><span class="sector-tag">{sector}</span></td>
                            <td>{logic}</td>
                        </tr>''')
        
        keypoints_pattern = r'(<table class="summary-table">\s*<thead>.*?</thead>\s*<tbody>)\s*.*?\s*(</tbody>\s*</table>)'
        keypoints_replacement = r'\1\n' + '\n'.join(tbody_rows) + r'\n                \2'
        new_content = re.sub(keypoints_pattern, keypoints_replacement, new_content, flags=re.DOTALL)
    
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

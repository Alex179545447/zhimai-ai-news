# -*- coding: utf-8 -*-
"""
智脉AI新闻API - 阿里云函数计算
用于实时抓取基于用户自定义标签的新闻
"""

import json
import requests
from datetime import datetime

# 智谱API配置
API_KEY = "28133690e57f4ba9902b4015f21404bb.L3eQw0LRHCFM7N9f"
API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

def fetch_news_by_tags(tags):
    """调用智谱GLM-4 API获取新闻"""
    today = datetime.now()
    date_str = today.strftime('%Y年%m月%d日')
    weekdays = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六']
    weekday = weekdays[today.weekday()]
    
    tags_str = "、".join(tags[:10])  # 最多10个标签
    
    prompt = f"""请搜索今天({date_str} {weekday})的最新新闻，重点关注以下用户兴趣标签：{tags_str}

要求：
1. 只搜索最近24小时内的新闻
2. 返回与用户兴趣标签相关的新闻
3. 每条新闻需包含：标题、日期、来源、摘要(50字内)、原文链接

请按以下JSON格式返回（只返回JSON，不要其他内容）：
{{
  "success": true,
  "tags": ["标签1", "标签2"],
  "count": 数量,
  "news": [
    {{"title": "新闻标题", "date": "日期时间", "source": "来源", "desc": "摘要", "url": "链接", "matchedTag": "匹配的标签"}}
  ],
  "generatedAt": "生成时间"
}}"""

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
            timeout=120
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            
            # 提取JSON
            import re
            json_match = re.search(r'```json\s*([\s\S]*?)\s*```', content) or re.search(r'\{[\s\S]*\}', content)
            if json_match:
                try:
                    return json.loads(json_match.group(0))
                except:
                    pass
            
            return {
                "success": False,
                "error": "无法解析API响应",
                "raw": content[:500]
            }
        else:
            return {
                "success": False,
                "error": f"API错误: {response.status_code}"
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def handler(environ, start_response):
    """阿里云函数计算入口函数"""
    method = environ.get('REQUEST_METHOD', 'GET')
    path = environ.get('PATH_INFO', '/')
    
    # CORS头
    headers = [
        ('Content-Type', 'application/json'),
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Methods', 'GET, POST, OPTIONS'),
        ('Access-Control-Allow-Headers', 'Content-Type')
    ]
    
    # 处理OPTIONS请求
    if method == 'OPTIONS':
        start_response('200 OK', headers)
        return [b'']
    
    # 健康检查
    if path == '/health' or path == '/':
        response_data = {
            "status": "ok",
            "service": "zhimai-news-api",
            "timestamp": datetime.now().isoformat()
        }
        start_response('200 OK', headers)
        return [json.dumps(response_data, ensure_ascii=False).encode('utf-8')]
    
    # 新闻API端点
    if path == '/api/news':
        try:
            # 获取请求体
            if method == 'POST':
                try:
                    request_body_size = int(environ.get('CONTENT_LENGTH', 0))
                    request_body = environ['wsgi.input'].read(request_body_size)
                    body = json.loads(request_body.decode('utf-8'))
                except:
                    body = {}
                
                tags = body.get('tags', [])
                
                if not tags or len(tags) == 0:
                    response_data = {"success": False, "error": "请提供至少一个标签"}
                    start_response('400 Bad Request', headers)
                    return [json.dumps(response_data, ensure_ascii=False).encode('utf-8')]
                
                if len(tags) > 10:
                    response_data = {"success": False, "error": "最多支持10个标签"}
                    start_response('400 Bad Request', headers)
                    return [json.dumps(response_data, ensure_ascii=False).encode('utf-8')]
                
                # 调用API获取新闻
                result = fetch_news_by_tags(tags)
                start_response('200 OK', headers)
                return [json.dumps(result, ensure_ascii=False).encode('utf-8')]
            else:
                response_data = {"error": "仅支持POST请求"}
                start_response('405 Method Not Allowed', headers)
                return [json.dumps(response_data, ensure_ascii=False).encode('utf-8')]
        except Exception as e:
            response_data = {"success": False, "error": str(e)}
            start_response('500 Internal Server Error', headers)
            return [json.dumps(response_data, ensure_ascii=False).encode('utf-8')]
    
    # 默认404
    response_data = {"error": "Not Found", "paths": ["/health", "/api/news"]}
    start_response('404 Not Found', headers)
    return [json.dumps(response_data, ensure_ascii=False).encode('utf-8')]


# 本地测试用
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    
    print("启动本地服务器: http://localhost:8080")
    print("按 Ctrl+C 停止服务器")
    
    httpd = make_server('', 8080, handler)
    httpd.serve_forever()

/**
 * 智脉AI新闻API - Cloudflare Worker
 * 用于实时抓取基于用户自定义标签的新闻
 */

const API_KEY = "28133690e57f4ba9902b4015f21404bb.L3eQw0LRHCFM7N9f";
const API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions";

// 允许的来源（防止滥用）
const ALLOWED_ORIGINS = [
  'https://daily.zhimai-ai.cn',
  'http://localhost:',
  'https://dashboard.zhimai-ai.cn'
];

async function fetchNewsByTags(tags) {
  const today = new Date();
  const dateStr = today.toLocaleDateString('zh-CN', { 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  });
  const weekdays = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六'];
  const weekday = weekdays[today.getDay()];
  
  const tagsStr = tags.join('、');
  
  const prompt = `请搜索今天(${dateStr} ${weekday})的最新新闻，重点关注以下用户兴趣标签：${tagsStr}

要求：
1. 只搜索最近24小时内的新闻
2. 返回与用户兴趣标签相关的新闻
3. 每条新闻需包含：标题、日期、来源、摘要(50字内)、原文链接

请按以下JSON格式返回（只返回JSON，不要其他内容）：
{
  "success": true,
  "tags": ["标签1", "标签2"],
  "count": 数量,
  "news": [
    {"title": "新闻标题", "date": "日期时间", "source": "来源", "desc": "摘要", "url": "链接", "matchedTag": "匹配的标签"}
  ],
  "generatedAt": "生成时间"
}`;

  const response = await fetch(API_URL, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${API_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      model: 'glm-4-flash',
      messages: [
        {
          role: 'user',
          content: prompt
        }
      ],
      tools: [
        {
          type: 'web_search',
          web_search: {
            search_engine: 'bing'
          }
        }
      ],
      stream: false
    })
  });

  if (!response.ok) {
    throw new Error(`API请求失败: ${response.status}`);
  }

  const result = await response.json();
  const content = result.choices?.[0]?.message?.content || '';
  
  // 提取JSON
  const jsonMatch = content.match(/```json\s*([\s\S]*?)\s*```/) || content.match(/\{[\s\S]*\}/);
  if (jsonMatch) {
    try {
      return JSON.parse(jsonMatch[0]);
    } catch (e) {
      console.error('JSON解析失败:', e);
    }
  }
  
  return {
    success: false,
    error: '无法解析API响应',
    raw: content
  };
}

async function handleRequest(request) {
  // CORS预检
  if (request.method === 'OPTIONS') {
    return new Response(null, {
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
      }
    });
  }

  const url = new URL(request.url);
  
  // 记录请求日志
  console.log(`[${new Date().toISOString()}] 请求: ${request.method} ${url.pathname}`);

  // 健康检查
  if (url.pathname === '/health') {
    return new Response(JSON.stringify({
      status: 'ok',
      service: 'zhimai-news-api',
      timestamp: new Date().toISOString()
    }), {
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      }
    });
  }

  // 新闻API端点
  if (url.pathname === '/api/news') {
    try {
      const body = await request.json();
      const tags = body.tags || [];
      
      if (!tags || tags.length === 0) {
        return new Response(JSON.stringify({
          success: false,
          error: '请提供至少一个标签'
        }), {
          status: 400,
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
          }
        });
      }

      if (tags.length > 10) {
        return new Response(JSON.stringify({
          success: false,
          error: '最多支持10个标签'
        }), {
          status: 400,
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
          }
        });
      }

      console.log(`正在搜索标签: ${tags.join(', ')}`);
      const result = await fetchNewsByTags(tags);
      
      return new Response(JSON.stringify(result), {
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Cache-Control': 'no-store'
        }
      });

    } catch (error) {
      console.error('请求处理错误:', error);
      return new Response(JSON.stringify({
        success: false,
        error: error.message || '服务器内部错误'
      }), {
        status: 500,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        }
      });
    }
  }

  // 默认404
  return new Response(JSON.stringify({
    error: 'Not Found',
    paths: ['/health', '/api/news']
  }), {
    status: 404,
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*'
    }
  });
}

addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request));
});

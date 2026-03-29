# 智脉AI新闻API - Cloudflare Worker部署指南

## 部署步骤

### 1. 注册Cloudflare账号
访问 https://dash.cloudflare.com/sign-up 注册（支持QQ邮箱）

### 2. 安装Wrangler CLI
```bash
npm install -g wrangler
```

### 3. 登录Cloudflare
```bash
wrangler login
```
这会打开浏览器，按提示授权即可。

### 4. 部署Worker
```bash
cd cloudflare-worker
wrangler deploy
```

部署成功后会返回类似：
```
https://zhimai-news-api.你的账号.workers.dev
```

### 5. 设置自定义域名（可选）
1. 在Cloudflare Dashboard中进入Worker设置
2. 选择"触发器" → "自定义域"
3. 添加如 `api.zhimai-ai.cn`
4. 在域名服务商添加CNAME记录指向

## API使用

### 健康检查
```
GET https://zhimai-news-api.你的账号.workers.dev/health
```

### 搜索新闻
```
POST https://zhimai-news-api.你的账号.workers.dev/api/news
Content-Type: application/json

{
  "tags": ["半导体", "AI大模型", "新能源汽车"]
}
```

### 响应示例
```json
{
  "success": true,
  "tags": ["半导体", "AI大模型"],
  "count": 3,
  "news": [
    {
      "title": "AI大模型日活突破千万",
      "date": "2026-03-30",
      "source": "腾讯新闻",
      "desc": "国产大模型用户活跃度持续攀升...",
      "url": "https://...",
      "matchedTag": "AI大模型"
    }
  ]
}
```

## 费用说明
- Cloudflare Worker免费额度：每天10万次请求
- 完全足够个人/小团队使用

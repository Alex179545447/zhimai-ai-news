# 智脉AI新闻API - 阿里云函数计算部署指南

## 阿里云函数计算优势
- ✅ 国内访问速度快
- ✅ 免费额度：每月40万GB-秒 + 100万次调用
- ✅ 自动弹性伸缩
- ✅ 按需付费，超低成本

## 部署步骤

### 1. 注册阿里云账号
访问 https://www.aliyun.com 用支付宝/淘宝账号注册

### 2. 开通函数计算服务
1. 进入 https://fc.console.aliyun.com/
2. 首次使用需要开通服务（免费）

### 3. 创建函数

#### 方式一：HTTP函数（推荐，最简单）
1. 点击 **"创建函数"**
2. 选择 **"HTTP Function"**
3. 配置：
   - 函数名称：`zhimai-news-api`
   - 请求处理程序（处理器）：`index.handler`
   - 运行语言：Python 3.10
   - 请求方法：GET, POST
   - 鉴权方式：无
4. 触发器配置：
   - 认证方式：无需认证
   - 勾选：允许 GET、POST、OPTIONS

#### 方式二：自定义运行时
1. 点击 **"创建函数"**
2. 选择 **"Custom Container"** 或 **"Custom Runtime"**
3. 上传代码包或使用命令行部署

### 4. 本地测试
```bash
cd aliyun-fc
pip install -r requirements.txt
python index.py
# 访问 http://localhost:8080/health 测试
```

### 5. 命令行部署（可选）
```bash
# 安装fun工具
npm install @alicloud/fun -g

# 配置凭证
fun config

# 部署
fun deploy
```

## API使用

### 健康检查
```
GET https://您的函数地址.REGION.fc.aliyuncs.com/2016-08-15/proxy/zhimai-news-api/default/health
```

### 搜索新闻
```
POST https://您的函数地址.REGION.fc.aliyuncs.com/2016-08-15/proxy/zhimai-news-api/default/api/news
Content-Type: application/json

{
  "tags": ["半导体", "AI大模型", "新能源汽车"]
}
```

## 免费额度说明
| 资源 | 免费额度/月 |
|------|------------|
| 调用次数 | 100万次 |
| 执行时长 | 40万GB-秒 |
| 公网流量 | 5GB |

完全足够个人或小团队使用！

## 注意事项
1. 函数计算有超时限制（默认60秒），智谱API搜索可能需要30-60秒
2. 建议在阿里云控制台将超时时间调整为120秒
3. 记得设置环境变量存储API Key（更安全）

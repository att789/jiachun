# API 接口文档

## 基本信息

**Base URL**: `http://localhost:3000`  
**版本**: v1.0.0  
**协议**: HTTP/HTTPS  
**数据格式**: JSON  
**字符编码**: UTF-8  

---

## 认证说明

### Session 认证

管理接口需要先登录获取 Session。

**登录流程**:
1. POST `/login` 获取 Session
2. 后续请求自动携带 Session Cookie
3. GET `/logout` 注销 Session

---

## 接口列表

### 1. 公开接口（无需登录）

#### 1.1 生成编码

**接口**: `POST /api/generate`  
**说明**: 生成本周编码映射表  
**认证**: 不需要  

**请求示例**:
```bash
curl -X POST http://localhost:3000/api/generate
```

**响应示例**:
```json
{
  "success": true,
  "message": "成功生成 2026年第37周编码",
  "data": {
    "year": 2026,
    "week": 37,
    "date": "2026-09-09",
    "mapping": {
      "荣信化工": "A",
      "兖矿荣信化工": "B",
      "内蒙古黄陶勒盖煤炭有限责任公司": "C"
    }
  }
}
```

**错误响应**:
```json
{
  "success": false,
  "message": "厂家列表为空，请先添加厂家"
}
```

---

#### 1.2 获取厂家列表

**接口**: `GET /api/suppliers`  
**说明**: 获取所有厂家列表  
**认证**: 不需要  

**请求示例**:
```bash
curl http://localhost:3000/api/suppliers
```

**响应示例**:
```json
{
  "success": true,
  "data": [
    "荣信化工",
    "兖矿荣信化工",
    "内蒙古黄陶勒盖煤炭有限责任公司"
  ]
}
```

---

### 2. 管理接口（需要登录）

#### 2.1 添加厂家

**接口**: `POST /api/suppliers/add`  
**说明**: 添加新厂家  
**认证**: 需要登录  

**请求参数**:
```json
{
  "name": "新厂家名称"
}
```

**请求示例**:
```bash
curl -X POST http://localhost:3000/api/suppliers/add \
  -H "Content-Type: application/json" \
  -d '{"name":"新疆新能源有限公司"}' \
  --cookie "session=..."
```

**响应示例**:
```json
{
  "success": true,
  "message": "成功添加厂家：新疆新能源有限公司"
}
```

**错误响应**:
```json
// 未登录
{
  "success": false,
  "message": "未授权"
}

// 厂家已存在
{
  "success": false,
  "message": "厂家已存在"
}

// 名称为空
{
  "success": false,
  "message": "厂家名称不能为空"
}
```

---

#### 2.2 删除厂家

**接口**: `POST /api/suppliers/delete`  
**说明**: 删除指定厂家  
**认证**: 需要登录  

**请求参数**:
```json
{
  "name": "要删除的厂家名称"
}
```

**请求示例**:
```bash
curl -X POST http://localhost:3000/api/suppliers/delete \
  -H "Content-Type: application/json" \
  -d '{"name":"新疆新能源有限公司"}' \
  --cookie "session=..."
```

**响应示例**:
```json
{
  "success": true,
  "message": "成功删除厂家：新疆新能源有限公司"
}
```

**错误响应**:
```json
// 未登录
{
  "success": false,
  "message": "未授权"
}

// 厂家不存在
{
  "success": false,
  "message": "厂家不存在"
}
```

---

#### 2.3 修改密码

**接口**: `POST /api/password/change`  
**说明**: 修改管理员密码  
**认证**: 需要登录  

**请求参数**:
```json
{
  "old_password": "原密码",
  "new_password": "新密码"
}
```

**请求示例**:
```bash
curl -X POST http://localhost:3000/api/password/change \
  -H "Content-Type: application/json" \
  -d '{"old_password":"admin123","new_password":"newpass123"}' \
  --cookie "session=..."
```

**响应示例**:
```json
{
  "success": true,
  "message": "密码修改成功"
}
```

**错误响应**:
```json
// 未登录
{
  "success": false,
  "message": "未授权"
}

// 原密码错误
{
  "success": false,
  "message": "原密码错误"
}

// 密码为空
{
  "success": false,
  "message": "密码不能为空"
}

// 密码太短
{
  "success": false,
  "message": "新密码长度至少6位"
}
```

---

### 3. 页面路由

#### 3.1 首页

**路由**: `GET /`  
**说明**: 显示本周编码映射表  
**认证**: 不需要  

**返回**: HTML 页面

---

#### 3.2 历史记录

**路由**: `GET /history`  
**说明**: 显示历史编码记录  
**认证**: 不需要  

**返回**: HTML 页面

---

#### 3.3 登录页面

**路由**: `GET /login`  
**说明**: 显示登录表单  
**认证**: 不需要  

**返回**: HTML 页面

---

#### 3.4 登录处理

**路由**: `POST /login`  
**说明**: 处理登录请求  
**认证**: 不需要  

**表单参数**:
- `password`: 管理员密码

**成功**: 重定向到 `/admin`  
**失败**: 返回登录页面并显示错误

---

#### 3.5 退出登录

**路由**: `GET /logout`  
**说明**: 清除 Session，退出登录  
**认证**: 不需要  

**成功**: 重定向到首页

---

#### 3.6 管理后台

**路由**: `GET /admin`  
**说明**: 管理后台页面  
**认证**: 需要登录  

**未登录**: 重定向到登录页  
**已登录**: 返回管理后台 HTML 页面

---

## 数据结构说明

### 编码数据结构

```json
{
  "year": 2026,           // 年份
  "week": 37,             // 周数（ISO 8601）
  "date": "2026-09-09",   // 生成日期
  "mapping": {            // 厂家-编码映射
    "厂家名称": "编码"
  }
}
```

### 厂家列表结构

```json
[
  "厂家名称1",
  "厂家名称2",
  "厂家名称3"
]
```

### 配置结构

```json
{
  "password_hash": "SHA256哈希值"
}
```

---

## 状态码说明

| 状态码 | 说明 |
|-------|------|
| 200 | 请求成功 |
| 401 | 未授权（需要登录） |
| 404 | 页面不存在 |
| 500 | 服务器错误 |

---

## 错误处理

所有 API 接口返回统一的错误格式：

```json
{
  "success": false,
  "message": "错误描述"
}
```

---

## 数据文件说明

### 1. 厂家列表 (`data/suppliers.json`)

```json
[
  "荣信化工",
  "兖矿荣信化工",
  "内蒙古黄陶勒盖煤炭有限责任公司"
]
```

### 2. 编码历史 (`data/codes_history.json`)

```json
[
  {
    "year": 2026,
    "week": 37,
    "date": "2026-09-09",
    "mapping": {
      "荣信化工": "A",
      "兖矿荣信化工": "B"
    }
  },
  {
    "year": 2026,
    "week": 36,
    "date": "2026-09-02",
    "mapping": {
      "荣信化工": "C",
      "兖矿荣信化工": "D"
    }
  }
]
```

**说明**: 
- 按时间倒序排列（最新的在前）
- 同一周重复生成会覆盖旧记录

### 3. 系统配置 (`data/config.json`)

```json
{
  "password_hash": "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918"
}
```

**说明**:
- `password_hash`: SHA256 加密的密码
- 默认密码 `admin123` 的哈希值

---

## 使用示例

### JavaScript (Fetch API)

```javascript
// 生成编码
fetch('http://localhost:3000/api/generate', {
  method: 'POST'
})
.then(res => res.json())
.then(data => {
  if (data.success) {
    console.log('生成成功:', data.data);
  } else {
    console.error('生成失败:', data.message);
  }
});

// 添加厂家（需要登录）
fetch('http://localhost:3000/api/suppliers/add', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  credentials: 'include', // 携带 Cookie
  body: JSON.stringify({
    name: '新厂家名称'
  })
})
.then(res => res.json())
.then(data => {
  alert(data.message);
});
```

### Python (requests)

```python
import requests

# 生成编码
response = requests.post('http://localhost:3000/api/generate')
data = response.json()
if data['success']:
    print('生成成功:', data['data'])
else:
    print('生成失败:', data['message'])

# 添加厂家（需要先登录）
session = requests.Session()
session.post('http://localhost:3000/login', data={'password': 'admin123'})

response = session.post('http://localhost:3000/api/suppliers/add', json={
    'name': '新厂家名称'
})
data = response.json()
print(data['message'])
```

### curl

```bash
# 生成编码
curl -X POST http://localhost:3000/api/generate

# 获取厂家列表
curl http://localhost:3000/api/suppliers

# 登录
curl -c cookies.txt -X POST http://localhost:3000/login \
  -d "password=admin123"

# 添加厂家（使用已保存的 Cookie）
curl -b cookies.txt -X POST http://localhost:3000/api/suppliers/add \
  -H "Content-Type: application/json" \
  -d '{"name":"新厂家名称"}'
```

---

## 扩展建议

### 后续可添加的 API

#### 1. 查询指定周编码
```
GET /api/codes/:year/:week
```

#### 2. 批量导入厂家
```
POST /api/suppliers/import
Body: { "suppliers": ["厂家1", "厂家2"] }
```

#### 3. 导出编码（Excel）
```
GET /api/export/excel/:year/:week
```

#### 4. 获取统计数据
```
GET /api/statistics
```

#### 5. 操作日志
```
GET /api/logs
```

---

## 安全建议

### 生产环境部署

1. **启用 HTTPS**
   ```python
   # 使用 SSL 证书
   app.run(ssl_context=('cert.pem', 'key.pem'))
   ```

2. **设置 CORS**
   ```python
   from flask_cors import CORS
   CORS(app, origins=['https://yourdomain.com'])
   ```

3. **添加请求限流**
   ```python
   from flask_limiter import Limiter
   limiter = Limiter(app, default_limits=["100 per hour"])
   ```

4. **添加 API Token 认证**
   ```python
   @app.before_request
   def check_token():
       if request.path.startswith('/api/'):
           token = request.headers.get('X-API-Token')
           if not verify_token(token):
               return jsonify({'error': 'Invalid token'}), 401
   ```

---

## 更新日志

### v1.0.0 (2026-09-09)
- ✅ 初始版本
- ✅ 基础 API 接口
- ✅ Session 认证
- ✅ 编码生成
- ✅ 厂家管理
- ✅ 密码管理

---

**文档版本**: v1.0.0  
**最后更新**: 2026-09-09  
**维护者**: Claude Code

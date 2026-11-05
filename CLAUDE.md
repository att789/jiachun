# 精甲醇厂家周编码系统 - 项目指引

## 📋 项目概述

**项目名称**：精甲醇厂家周编码系统  
**开发日期**：2026-09-09  
**技术栈**：Python 3.8+ + Flask 3.0 + Bootstrap 5  
**项目类型**：Web 应用（最小化组件设计）  
**数据存储**：JSON 文件  

---

## 🎯 项目目标

为精甲醇行业提供一个**每周自动生成厂家编码映射表**的管理系统，编码规则为：
- 排除易混淆字母：D, I, J, L, O, U, V, Z
- 使用 18 个允许字母：A, B, C, E, F, G, H, K, M, N, P, Q, R, S, T, W, X, Y
- 支持 1-342 个厂家（单字母 18 个 + 双字母 324 个）
- 每周编码自动失效，需重新生成

---

## 📁 项目结构

```
D:\work\jiachun\
├── app.py                          # Flask 应用主入口（265行）
├── requirements.txt                # Python 依赖（Flask==3.0.0）
├── README.md                       # 项目说明文档
├── CLAUDE.md                       # 本文档 - 项目指引
├── 项目交付文档.md                  # 详细交付文档
│
├── 启动脚本（4个）:
│   ├── run.bat                    # 推荐使用 - 超简单版（纯英文）
│   ├── start.bat                  # 智能版（自动查找Python）
│   ├── 快速启动.bat               # 备用方案
│   └── 启动系统.bat               # 原版（可能有中文显示问题）
│
├── core/                          # 核心业务逻辑模块
│   ├── __init__.py
│   ├── generator.py              # 编码生成器（118行）
│   │   └── CodeGenerator         # 编码生成类
│   └── storage.py                # 数据存储器（98行）
│       └── Storage               # JSON 存储类
│
├── auth/                         # 认证模块
│   ├── __init__.py
│   └── password.py               # 密码管理（50行）
│       └── PasswordAuth          # 密码认证类
│
├── routes/                       # 路由模块（预留扩展）
│   └── __init__.py
│
├── templates/                    # Jinja2 前端模板
│   ├── layout.html              # 基础布局模板（90行）
│   ├── index.html               # 首页 - 编码展示（150行）
│   ├── login.html               # 登录页（80行）
│   ├── admin.html               # 管理后台（200行）
│   ├── history.html             # 历史记录（110行）
│   ├── 404.html                 # 404 错误页（20行）
│   └── 500.html                 # 500 错误页（20行）
│
├── static/                      # 静态资源
│   └── style.css                # 工业风格样式（600行）
│
└── data/                        # 数据目录（运行时自动创建）
    ├── suppliers.json           # 厂家列表
    ├── codes_history.json       # 编码历史记录
    └── config.json              # 系统配置（密码哈希等）
```

---

## 🔧 核心模块说明

### 1. 编码生成器 (`core/generator.py`)

**类名**：`CodeGenerator`

**核心方法**：
```python
@staticmethod
def generate(suppliers: list) -> dict:
    """生成周编码"""
    # 返回: {
    #   'year': 2026,
    #   'week': 37,
    #   'date': '2026-09-09',
    #   'mapping': {'厂家名': '编码', ...}
    # }
```

**算法逻辑**：
1. 定义允许的 18 个字母（排除 DIJLOUVZ）
2. 生成单字母池（18个）和双字母池（324个）
3. 使用 Fisher-Yates 洗牌算法打乱顺序
4. 根据厂家数量分配编码
5. 返回年、周、日期和映射关系

**支持范围**：1-342 个厂家

---

### 2. 数据存储器 (`core/storage.py`)

**类名**：`Storage`

**核心方法**：
```python
def load_suppliers() -> list          # 加载厂家列表
def save_suppliers(suppliers: list)   # 保存厂家列表
def save_codes(codes_data: dict)      # 保存编码历史
def get_current_codes() -> dict       # 获取本周编码
def get_history(limit: int) -> list   # 获取历史记录
def get_codes_by_week(year, week)     # 获取指定周编码
```

**存储格式**：
- `suppliers.json` - 厂家列表（字符串数组）
- `codes_history.json` - 编码历史（对象数组，按时间倒序）
- `config.json` - 系统配置（密码哈希）

---

### 3. 密码认证 (`auth/password.py`)

**类名**：`PasswordAuth`

**核心方法**：
```python
@staticmethod
def verify(password: str) -> bool              # 验证密码
@staticmethod
def change_password(old, new) -> bool          # 修改密码
@staticmethod
def hash_password(password: str) -> str        # SHA256 哈希
```

**安全特性**：
- 使用 SHA256 加密存储密码
- 默认密码：`admin123`
- 密码存储在 `data/config.json`

---

### 4. Flask 应用 (`app.py`)

**路由结构**：

#### 公开路由（无需登录）
- `GET /` - 首页，显示本周编码
- `GET /history` - 历史记录页面
- `GET /login` - 登录页面
- `POST /login` - 处理登录

#### 管理路由（需登录）
- `GET /admin` - 管理后台
- `GET /logout` - 退出登录

#### API 路由
- `POST /api/generate` - 生成本周编码
- `GET /api/suppliers` - 获取厂家列表
- `POST /api/suppliers/add` - 添加厂家（需登录）
- `POST /api/suppliers/delete` - 删除厂家（需登录）
- `POST /api/password/change` - 修改密码（需登录）

#### 错误处理
- `404` - 页面不存在
- `500` - 服务器错误

---

## 🎨 前端设计

### 设计风格
- **主题**：工业风格深色主题
- **配色**：
  - 主色：`#1a2332`, `#2c3e50`（深蓝灰）
  - 强调色：`#ffc107`（金黄）, `#ff6b35`（橙色）
  - 功能色：绿色、红色、蓝色

### 核心组件
1. **导航栏** - Bootstrap navbar，深色背景
2. **工业卡片** - 渐变边框，阴影效果
3. **编码徽章** - 橙色渐变，发光动画
4. **表格** - 悬停高亮，平滑动画
5. **按钮** - 渐变色，悬停提升效果

### 动画效果
- `fade-in` - 淡入动画
- `slide-in` - 滑入动画
- `glow` - 发光脉冲
- `hover` - 悬停放大/提升

---

## 🚀 开发指南

### 启动开发环境

```bash
# 1. 安装依赖
pip install Flask

# 2. 启动开发服务器（带自动重载）
python app.py

# 3. 访问系统
# http://localhost:3000
```

### 调试模式

在 `app.py` 中：
```python
app.run(host='0.0.0.0', port=3000, debug=True)  # debug=True 开启调试
```

---

## 🔨 如何添加新功能

### 1. 添加新路由

在 `app.py` 中添加：
```python
@app.route('/your-route')
def your_function():
    """你的功能描述"""
    # 你的逻辑
    return render_template('your_template.html', data=data)
```

### 2. 添加新页面

在 `templates/` 中创建新文件：
```html
{% extends "layout.html" %}

{% block title %}页面标题{% endblock %}

{% block content %}
<!-- 你的内容 -->
{% endblock %}
```

### 3. 添加新 API

```python
@app.route('/api/your-api', methods=['POST'])
def your_api():
    """你的 API 说明"""
    if not session.get('authenticated'):
        return jsonify({'success': False, 'message': '未授权'}), 401
    
    # 你的逻辑
    return jsonify({'success': True, 'data': data})
```

### 4. 添加新样式

在 `static/style.css` 中添加：
```css
.your-class {
    /* 你的样式 */
}
```

---

## 📦 部署指南

### 方式1: 开发环境运行
```bash
python app.py
```

### 方式2: 生产环境（Gunicorn）
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:3000 app:app
```

### 方式3: 打包成 exe
```bash
pip install pyinstaller
pyinstaller --onefile --add-data "templates;templates" --add-data "static;static" --name "精甲醇编码系统" app.py
```

### 方式4: Docker 部署
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 3000
CMD ["python", "app.py"]
```

---

## 🐛 已知问题与解决方案

### 1. Windows CMD 字符编码问题
**问题**：启动脚本显示乱码或闪退  
**解决**：使用 `run.bat`（纯英文版）

### 2. Python 路径未找到
**问题**：提示 `python` 不是内部或外部命令  
**解决**：
- 使用 `py -3 app.py` 代替 `python app.py`
- 或重新安装 Python 并勾选 "Add Python to PATH"

### 3. 端口被占用
**问题**：启动失败，提示端口 3000 已被占用  
**解决**：修改 `app.py` 中的端口号：
```python
app.run(host='0.0.0.0', port=8080, debug=True)  # 改为 8080
```

### 4. 忘记管理密码
**问题**：无法登录管理后台  
**解决**：删除 `data/config.json` 文件，密码重置为 `admin123`

---

## 🔐 安全建议

### 生产环境部署时：

1. **修改默认密码**
   - 首次登录后立即修改密码

2. **关闭调试模式**
   ```python
   app.run(host='0.0.0.0', port=3000, debug=False)
   ```

3. **设置强密码**
   ```python
   # 修改 secret_key
   app.secret_key = 'your-very-strong-random-secret-key-here'
   ```

4. **使用 HTTPS**
   - 配置 SSL 证书
   - 使用 Nginx 反向代理

5. **限制访问 IP**
   - 在 Nginx 或防火墙层面限制

6. **定期备份数据**
   ```bash
   # 备份 data 目录
   cp -r data/ backup/data_$(date +%Y%m%d)/
   ```

---

## 🎯 扩展功能建议

### 后续可实现的功能：

#### 1. 定时任务
```python
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.add_job(
    func=auto_generate_codes,
    trigger='cron',
    day_of_week='mon',
    hour=0,
    minute=0
)
scheduler.start()
```

#### 2. Excel 导出
```python
import openpyxl

def export_to_excel(codes_data):
    wb = openpyxl.Workbook()
    ws = wb.active
    # ... 写入数据
    wb.save('codes.xlsx')
```

#### 3. 邮件通知
```python
import smtplib
from email.mime.text import MIMEText

def send_notification(codes_data):
    # 发送编码表到指定邮箱
    pass
```

#### 4. 数据统计
- 添加图表展示（使用 Chart.js）
- 统计各厂家编码使用频率
- 历史趋势分析

#### 5. 厂家分组管理
- 支持厂家分类（如：内蒙、新疆、陕西）
- 分组生成编码
- 批量导入厂家

---

## 📚 技术栈文档

### Python Flask
- [Flask 官方文档](https://flask.palletsprojects.com/)
- [Jinja2 模板引擎](https://jinja.palletsprojects.com/)

### Bootstrap 5
- [Bootstrap 5 文档](https://getbootstrap.com/)
- [Bootstrap Icons](https://icons.getbootstrap.com/)

### JavaScript
- [MDN Web Docs](https://developer.mozilla.org/)

---

## 🤝 开发约定

### 代码风格
- Python: PEP 8 规范
- HTML: 使用 2 空格缩进
- CSS: BEM 命名规范
- JavaScript: ES6+ 标准

### Git 提交规范
```
feat: 新功能
fix: 修复 bug
docs: 文档更新
style: 代码格式调整
refactor: 重构代码
test: 测试相关
chore: 构建/工具相关
```

### 注释规范
```python
def function_name(param: type) -> return_type:
    """
    函数简短描述
    
    Args:
        param: 参数说明
    
    Returns:
        返回值说明
    """
```

---

## 📞 技术支持

### 常见问题
请参考 `README.md` 的"常见问题"章节

### 开发文档
- `README.md` - 用户使用文档
- `CLAUDE.md` - 本文档，开发指引
- `项目交付文档.md` - 详细交付说明

---

## 📝 更新日志

### v1.0.0 (2026-09-09)
- ✨ 首次发布
- ✅ 完整的编码生成功能
- ✅ 精美的工业风格界面
- ✅ 完善的管理后台
- ✅ 历史记录功能
- ✅ 数据导出功能
- ✅ 密码保护功能
- ✅ 4种启动脚本（兼容性优化）

---

## 🎉 快速开始

```bash
# 1. 启动系统
双击: run.bat

# 2. 浏览器访问
http://localhost:3000

# 3. 登录管理
密码: admin123

# 4. 开始使用
- 查看本周编码
- 管理厂家名单
- 生成新编码
- 导出编码表
```

---

**文档版本**: v1.0.0  
**最后更新**: 2026-09-09  
**维护者**: Claude Code

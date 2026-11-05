# 精甲醇厂家周编码系统

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.0-purple.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**一个现代化的精甲醇厂家周编码管理系统**

[功能特性](#功能特性) • [快速开始](#快速开始) • [使用说明](#使用说明) • [技术架构](#技术架构)

</div>

---

## 📋 功能特性

### 核心功能
- ✅ **自动编码生成** - 每周自动生成随机编码映射表
- ✅ **厂家管理** - 支持厂家的增删改查
- ✅ **历史记录** - 保存所有历史编码记录
- ✅ **数据导出** - 支持导出为文本格式
- ✅ **密码保护** - 管理后台密码保护

### 编码规则
- 排除易混淆字母：`D, I, J, L, O, U, V, Z`
- 使用字母：`A, B, C, E, F, G, H, K, M, N, P, Q, R, S, T, W, X, Y`（18个）
- 编码方式：
  - 厂家数 ≤ 18：使用单字母（A-Y）
  - 厂家数 > 18：单字母 + 双字母组合（最多342个）
- 每周编码自动失效，需重新生成

### 界面特色
- 🎨 **工业风格设计** - 深色主题，科技感十足
- 📱 **响应式布局** - 支持桌面端和移动端
- ⚡ **流畅动画** - 平滑过渡和交互效果
- 🔔 **即时反馈** - 操作结果实时提示

---

## 🚀 快速开始

### 环境要求

- Python 3.8 或更高版本
- pip 包管理器

### 安装步骤

#### 方式1: 使用启动脚本（推荐）

1. **克隆或下载项目**
   ```bash
   # 如果使用 Git
   git clone <项目地址>
   cd methanol-coding-system
   ```

2. **双击运行启动脚本**
   ```
   双击：启动系统.bat
   ```

#### 方式2: 手动安装

1. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

2. **启动系统**
   ```bash
   python app.py
   ```

3. **访问系统**
   ```
   浏览器打开: http://localhost:3000
   ```

### 首次使用

- **默认管理密码**: `admin123`
- **建议**: 首次登录后立即修改密码

---

## 📖 使用说明

### 1. 查看编码（公开访问）

- **首页**: 显示本周编码映射表
- **历史记录**: 查看历史周编码
- **导出功能**: 下载编码表为文本文件

### 2. 管理后台（需登录）

#### 登录管理
1. 点击右上角 "管理登录"
2. 输入密码（默认：admin123）
3. 登录成功后进入管理后台

#### 厂家管理
- **添加厂家**: 点击"添加厂家"按钮
- **删除厂家**: 点击厂家列表中的"删除"按钮

#### 生成编码
- 点击"生成本周编码"按钮
- 系统自动根据当前厂家列表生成编码
- 同一周重复生成会覆盖旧编码

#### 修改密码
1. 点击"修改密码"
2. 输入原密码和新密码
3. 确认修改

---

## 🏗️ 技术架构

### 技术栈

```
后端：Python 3.8+ + Flask 3.0
前端：Bootstrap 5 + Jinja2 + 原生 JavaScript
数据：JSON 文件存储
样式：自定义工业风格 CSS
```

### 项目结构

```
methanol-coding-system/
├── app.py                      # 应用主入口
├── requirements.txt            # Python 依赖
├── 启动系统.bat                 # Windows 启动脚本
├── README.md                   # 项目说明文档
│
├── core/                       # 核心模块
│   ├── __init__.py
│   ├── generator.py           # 编码生成器
│   └── storage.py             # 数据存储
│
├── auth/                      # 认证模块
│   ├── __init__.py
│   └── password.py            # 密码管理
│
├── routes/                    # 路由模块
│   └── __init__.py
│
├── templates/                 # HTML 模板
│   ├── layout.html           # 基础布局
│   ├── index.html            # 首页
│   ├── login.html            # 登录页
│   ├── admin.html            # 管理后台
│   ├── history.html          # 历史记录
│   ├── 404.html              # 404 页面
│   └── 500.html              # 500 页面
│
├── static/                    # 静态资源
│   └── style.css             # 自定义样式
│
└── data/                      # 数据目录（自动创建）
    ├── suppliers.json        # 厂家列表
    ├── codes_history.json    # 编码历史
    └── config.json           # 系统配置
```

### 核心算法

#### 编码生成算法
```python
def generate(suppliers: list) -> dict:
    """
    1. 定义允许的字母（18个）
    2. 生成单字母池（18个）
    3. 生成双字母池（324个）
    4. Fisher-Yates 洗牌算法随机排序
    5. 按需分配编码给厂家
    """
```

#### 数据存储
```python
# JSON 文件结构
{
  "year": 2026,
  "week": 36,
  "date": "2026-09-09",
  "mapping": {
    "荣信化工": "A",
    "兖矿荣信化工": "B",
    ...
  }
}
```

---

## 🎨 界面预览

### 首页 - 编码查看
- 显示当前周编码映射表
- 支持导出和刷新
- 统计卡片展示关键信息

### 管理后台
- 厂家列表管理
- 快速操作面板
- 历史记录概览

### 历史记录
- 时间轴展示
- 可折叠详情
- 支持导出历史编码

---

## ⚙️ 配置说明

### 端口配置
默认端口：`3000`

修改端口：编辑 `app.py` 文件最后一行
```python
app.run(host='0.0.0.0', port=3000, debug=True)  # 修改 port 值
```

### 初始厂家列表
系统首次运行会自动导入36家默认厂家，在 `app.py` 中的 `initial_suppliers` 列表中定义。

### 密码配置
- 默认密码：`admin123`
- 首次登录后建议立即修改
- 密码使用 SHA256 加密存储

---

## 📦 部署方案

### 方案1: 本地运行（开发/测试）
```bash
python app.py
```

### 方案2: 生产环境部署
使用 Gunicorn（推荐）
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:3000 app:app
```

### 方案3: 打包成 exe
```bash
pip install pyinstaller
pyinstaller --onefile --add-data "templates;templates" --add-data "static;static" --name "精甲醇编码系统" app.py
```
生成的 exe 文件在 `dist/` 目录中。

---

## 🔧 常见问题

### Q: 启动时提示"Python未安装"？
**A**: 请先安装 Python 3.8+，下载地址：https://www.python.org/downloads/

### Q: 启动失败，提示端口被占用？
**A**: 修改 `app.py` 中的端口号，或关闭占用 3000 端口的程序。

### Q: 忘记管理密码怎么办？
**A**: 删除 `data/config.json` 文件，密码会重置为默认的 `admin123`。

### Q: 如何备份数据？
**A**: 备份整个 `data/` 目录即可，包含所有厂家和历史记录。

### Q: 编码为什么每周都要重新生成？
**A**: 这是系统设计的安全特性，确保编码定期更新，防止长期使用同一编码。

---

## 🔐 安全说明

1. **密码存储**: 使用 SHA256 加密，不存储明文
2. **会话管理**: 使用 Flask Session，自动超时
3. **数据隔离**: 管理功能需要登录验证
4. **建议**: 在生产环境中使用 HTTPS 协议

---

## 🛠️ 开发指南

### 添加新功能

1. **添加新路由**
   ```python
   # 在 app.py 中添加
   @app.route('/your-route')
   def your_function():
       return render_template('your_template.html')
   ```

2. **添加新模板**
   ```html
   <!-- 在 templates/ 中创建新文件 -->
   {% extends "layout.html" %}
   {% block content %}
   <!-- 你的内容 -->
   {% endblock %}
   ```

3. **添加新样式**
   ```css
   /* 在 static/style.css 中添加 */
   .your-class {
       /* 你的样式 */
   }
   ```

### 调试模式

开启调试：`app.py` 中设置 `debug=True`（默认已开启）
```python
app.run(host='0.0.0.0', port=3000, debug=True)
```

---

## 📝 更新日志

### v1.0.0 (2026-09-09)
- ✨ 初始版本发布
- ✅ 核心编码生成功能
- ✅ 厂家管理功能
- ✅ 历史记录查看
- ✅ 管理后台
- ✅ 密码保护
- ✅ 数据导出
- ✅ 工业风格界面

---

## 📄 开源协议

MIT License

---

## 👨‍💻 作者

开发者：Claude Code  
技术栈：Python + Flask + Bootstrap 5  
开发时间：2026年9月

---

## 💬 反馈与支持

如有问题或建议，欢迎反馈！

---

<div align="center">

**精甲醇厂家周编码系统** - 让编码管理更简单

⭐ 如果这个项目对你有帮助，请给个 Star！

</div>

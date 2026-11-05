# 精甲醇厂家周编码系统 - Python 技术栈实现方案

## 📋 方案概述

本文档提供使用 **Python + Flask + Bootstrap** 技术栈实现精甲醇厂家周编码系统的完整方案。

### 与 Node.js 方案对比

| 对比项 | Python 方案 | Node.js 方案（当前） |
|--------|------------|-------------------|
| **后端框架** | Flask | Express.js |
| **前端技术** | Jinja2 + Bootstrap | Vue 3 + Element Plus |
| **数据存储** | JSON / SQLite | JSON |
| **打包部署** | PyInstaller → exe | 绿色版部署 |
| **文件大小** | ~30MB (单exe) | ~50MB (含Node.js) |
| **开发速度** | ⭐⭐⭐⭐⭐ 很快 | ⭐⭐⭐⭐ 快 |
| **部署难度** | ⭐⭐⭐⭐⭐ 极简单 | ⭐⭐⭐⭐ 简单 |
| **前端现代化** | ⭐⭐⭐ 传统模板 | ⭐⭐⭐⭐⭐ 现代SPA |
| **学习曲线** | ⭐⭐⭐⭐⭐ 最简单 | ⭐⭐⭐ 中等 |

---

## 🛠️ 技术栈选择

### 后端框架：Flask

**选择理由：**
- ✅ 轻量级，适合小型项目
- ✅ 语法简洁，易于维护
- ✅ 生态丰富，插件众多
- ✅ 学习曲线平缓
- ✅ 内置开发服务器

**核心依赖：**
```python
Flask==3.0.0           # Web框架
Flask-CORS==4.0.0      # 跨域支持
APScheduler==3.10.4    # 定时任务
PyJWT==2.8.0           # JWT认证
```

### 前端技术：Jinja2 + Bootstrap 5

**选择理由：**
- ✅ 服务端渲染，SEO友好
- ✅ Bootstrap 5 现代化UI
- ✅ 无需复杂构建工具
- ✅ 开发效率高
- ✅ 适合内网系统

### 数据存储：JSON / SQLite

**两种方案：**

#### 方案A：JSON 文件（推荐轻量级部署）
```python
import json

# 优点：
✅ 零依赖，无需安装数据库
✅ 易于备份和迁移
✅ 可直接查看编辑
✅ 适合小规模数据
```

#### 方案B：SQLite（推荐数据量大时）
```python
import sqlite3

# 优点：
✅ 内置数据库，无需安装
✅ SQL查询，功能强大
✅ 事务支持，数据安全
✅ 适合复杂查询
```

### 打包工具：PyInstaller

**一键打包成 exe：**
```bash
pip install pyinstaller
pyinstaller --onefile --windowed app.py
```

**优点：**
- ✅ 单文件 exe，超简单
- ✅ 文件体积小（~30MB）
- ✅ 无需安装 Python
- ✅ 启动快速（1-2秒）

---

## 📁 项目结构

```
methanol-coding-python/
├── app.py                      # 应用主入口
├── config.py                   # 配置文件
├── requirements.txt            # Python依赖
│
├── models/                     # 数据模型
│   ├── __init__.py
│   ├── database.py            # 数据库操作
│   ├── supplier.py            # 厂家模型
│   ├── code_history.py        # 编码历史模型
│   └── config.py              # 配置模型
│
├── routes/                     # 路由模块
│   ├── __init__.py
│   ├── main.py                # 主页路由
│   ├── api.py                 # API路由
│   ├── admin.py               # 管理后台路由
│   └── auth.py                # 认证路由
│
├── utils/                      # 工具函数
│   ├── __init__.py
│   ├── code_generator.py      # 编码生成算法
│   ├── date_helper.py         # 日期处理
│   ├── auth_helper.py         # 认证辅助
│   └── export_helper.py       # 导出功能
│
├── templates/                  # Jinja2 模板
│   ├── base.html              # 基础模板
│   ├── index.html             # 首页
│   ├── admin/
│   │   ├── dashboard.html     # 管理控制台
│   │   ├── history.html       # 历史记录
│   │   ├── suppliers.html     # 厂家管理
│   │   ├── logs.html          # 操作日志
│   │   └── settings.html      # 系统设置
│   └── components/
│       ├── navbar.html        # 导航栏
│       └── footer.html        # 页脚
│
├── static/                     # 静态资源
│   ├── css/
│   │   ├── style.css          # 自定义样式
│   │   └── industrial.css     # 工业风格主题
│   ├── js/
│   │   ├── main.js            # 主脚本
│   │   └── admin.js           # 管理后台脚本
│   └── images/
│       └── logo.png
│
├── data/                       # 数据目录
│   ├── database.json          # JSON数据库（方案A）
│   └── methanol.db            # SQLite数据库（方案B）
│
├── logs/                       # 日志目录
│   └── app.log
│
├── 启动系统.bat                # Windows启动脚本
├── 打包exe.bat                # 打包脚本
└── README_PYTHON.md           # Python版文档
```

---

## 💻 核心代码实现

### 1. 应用主入口（app.py）

```python
"""
精甲醇厂家周编码系统
Flask 应用主入口
"""

from flask import Flask, render_template, jsonify
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import os

from config import Config
from routes import main_bp, api_bp, admin_bp, auth_bp
from models.database import init_database
from utils.code_generator import generate_weekly_codes
from utils.date_helper import get_current_week

# 创建 Flask 应用
app = Flask(__name__)
app.config.from_object(Config)

# 启用 CORS
CORS(app)

# 初始化数据库
init_database()

# 注册蓝图（路由模块）
app.register_blueprint(main_bp)
app.register_blueprint(api_bp, url_prefix='/api')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(auth_bp, url_prefix='/auth')

# 定时任务调度器
scheduler = BackgroundScheduler()


def scheduled_generate_codes():
    """定时任务：生成周编码"""
    try:
        year, week = get_current_week()
        from models.supplier import get_active_suppliers
        from models.code_history import save_codes
        
        suppliers = get_active_suppliers()
        codes = generate_weekly_codes(suppliers)
        save_codes(year, week, codes)
        
        print(f'[定时任务] {datetime.now()} - 已生成 {year}年第{week}周编码')
    except Exception as e:
        print(f'[定时任务错误] {e}')


# 启动定时任务
def start_scheduler():
    """启动定时任务调度器"""
    from models.config import get_schedule_config
    
    cron_expr = get_schedule_config()
    # 解析 Cron 表达式: 分 时 日 月 周
    parts = cron_expr.split()
    
    if len(parts) == 5:
        minute, hour, day, month, day_of_week = parts
        
        scheduler.add_job(
            func=scheduled_generate_codes,
            trigger='cron',
            minute=minute,
            hour=hour,
            day=day if day != '*' else None,
            month=month if month != '*' else None,
            day_of_week=day_of_week if day_of_week != '*' else None,
            id='generate_codes'
        )
        
        scheduler.start()
        print(f'[定时任务] 已启动，Cron: {cron_expr}')


# 错误处理
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


# 健康检查
@app.route('/health')
def health_check():
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat()
    })


if __name__ == '__main__':
    # 启动定时任务
    start_scheduler()
    
    # 启动 Flask 应用
    port = int(os.environ.get('PORT', 3000))
    print(f'''
========================================
精甲醇厂家周编码系统 v1.0.0
========================================
访问地址: http://localhost:{port}
默认密码: admin123
按 Ctrl+C 停止服务
========================================
    ''')
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=Config.DEBUG
    )
```

---

### 2. 配置文件（config.py）

```python
"""
应用配置
"""

import os
from datetime import timedelta


class Config:
    """应用配置类"""
    
    # 基础配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'methanol-coding-secret-2026'
    DEBUG = os.environ.get('FLASK_ENV') == 'development'
    
    # 数据存储配置
    DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
    JSON_DATABASE = os.path.join(DATA_DIR, 'database.json')
    SQLITE_DATABASE = os.path.join(DATA_DIR, 'methanol.db')
    
    # 使用 JSON 还是 SQLite
    USE_JSON = True  # True: JSON, False: SQLite
    
    # JWT 配置
    JWT_SECRET = os.environ.get('JWT_SECRET') or 'jwt-secret-key-2026'
    JWT_EXPIRATION = timedelta(hours=8)  # Token 有效期 8 小时
    
    # 日志配置
    LOG_DIR = os.path.join(os.path.dirname(__file__), 'logs')
    LOG_FILE = os.path.join(LOG_DIR, 'app.log')
    
    # 编码生成规则
    ALLOWED_LETTERS = list('ABCEFGHKMNPQRSTWXY')  # 18个允许的字母
    EXCLUDED_LETTERS = list('DIJLOUVZ')  # 8个排除的字母
    
    # 分页配置
    ITEMS_PER_PAGE = 50
    
    # 上传配置
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    
    @staticmethod
    def init_app(app):
        """初始化应用配置"""
        # 确保目录存在
        os.makedirs(Config.DATA_DIR, exist_ok=True)
        os.makedirs(Config.LOG_DIR, exist_ok=True)
```

---

### 3. 编码生成算法（utils/code_generator.py）

```python
"""
编码生成算法
"""

import random
from config import Config


def generate_weekly_codes(suppliers):
    """
    生成周编码
    
    Args:
        suppliers: 厂家列表 [{'id': 1, 'name': '荣信化工'}, ...]
    
    Returns:
        dict: {厂家名称: 编码}
    """
    count = len(suppliers)
    
    if count == 0:
        return {}
    
    if count > 342:
        raise ValueError(f'厂家数量超出限制：{count} > 342')
    
    # 生成编码池
    codes = generate_code_pool(count)
    
    # Fisher-Yates 洗牌算法
    random.shuffle(codes)
    
    # 分配编码
    result = {}
    for i, supplier in enumerate(suppliers):
        result[supplier['name']] = codes[i]
    
    return result


def generate_code_pool(count):
    """
    生成编码池
    
    Args:
        count: 需要的编码数量
    
    Returns:
        list: 编码列表
    """
    letters = Config.ALLOWED_LETTERS
    codes = []
    
    # 单字母编码（18个）
    if count <= len(letters):
        return letters[:count]
    
    # 单字母 + 双字母编码
    codes.extend(letters)  # 先添加18个单字母
    
    # 生成所有双字母组合（324个）
    double_letters = [a + b for a in letters for b in letters]
    random.shuffle(double_letters)  # 打乱双字母顺序
    
    # 添加所需数量的双字母
    needed = count - len(letters)
    codes.extend(double_letters[:needed])
    
    return codes


def validate_code(code):
    """
    验证编码是否合法
    
    Args:
        code: 编码字符串
    
    Returns:
        bool: 是否合法
    """
    if not code:
        return False
    
    # 检查长度
    if len(code) not in [1, 2]:
        return False
    
    # 检查字符
    allowed = Config.ALLOWED_LETTERS
    return all(c in allowed for c in code)


# 测试代码
if __name__ == '__main__':
    # 测试生成编码
    test_suppliers = [
        {'id': i, 'name': f'厂家{i}'}
        for i in range(1, 37)
    ]
    
    codes = generate_weekly_codes(test_suppliers)
    
    print('生成的编码：')
    for name, code in codes.items():
        print(f'{name}: {code}')
    
    print(f'\n总数：{len(codes)}')
    print(f'包含排除字母：{any(c in Config.EXCLUDED_LETTERS for code in codes.values() for c in code)}')
```

---

### 4. 日期处理（utils/date_helper.py）

```python
"""
日期处理工具
"""

from datetime import datetime, date


def get_current_week():
    """
    获取当前周数（ISO 8601 标准）
    
    Returns:
        tuple: (年份, 周数)
    """
    today = date.today()
    iso_calendar = today.isocalendar()
    return iso_calendar[0], iso_calendar[1]


def get_week_date_range(year, week):
    """
    获取指定周的日期范围
    
    Args:
        year: 年份
        week: 周数
    
    Returns:
        tuple: (开始日期, 结束日期)
    """
    # ISO 8601: 每周从周一开始
    jan4 = date(year, 1, 4)
    week_one_monday = jan4 - timedelta(days=jan4.weekday())
    target_monday = week_one_monday + timedelta(weeks=week - 1)
    target_sunday = target_monday + timedelta(days=6)
    
    return target_monday, target_sunday


def format_datetime(dt):
    """
    格式化日期时间
    
    Args:
        dt: datetime 对象或字符串
    
    Returns:
        str: 格式化后的字符串
    """
    if isinstance(dt, str):
        return dt
    
    if isinstance(dt, datetime):
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    
    if isinstance(dt, date):
        return dt.strftime('%Y-%m-%d')
    
    return str(dt)


def parse_cron(cron_expr):
    """
    解析 Cron 表达式
    
    Args:
        cron_expr: Cron 表达式 "分 时 日 月 周"
    
    Returns:
        dict: 解析后的字典
    """
    parts = cron_expr.split()
    
    if len(parts) != 5:
        raise ValueError(f'无效的 Cron 表达式: {cron_expr}')
    
    return {
        'minute': parts[0],
        'hour': parts[1],
        'day': parts[2],
        'month': parts[3],
        'day_of_week': parts[4]
    }


# 测试代码
if __name__ == '__main__':
    year, week = get_current_week()
    print(f'当前：{year}年第{week}周')
    
    start, end = get_week_date_range(year, week)
    print(f'日期范围：{start} ~ {end}')
```

---

### 5. 数据库操作（models/database.py）

#### 方案A：JSON 存储

```python
"""
JSON 数据库操作
"""

import json
import os
from datetime import datetime
from config import Config


class JSONDatabase:
    """JSON 数据库类"""
    
    def __init__(self):
        self.db_file = Config.JSON_DATABASE
        self.data = self._load()
    
    def _load(self):
        """加载数据"""
        if os.path.exists(self.db_file):
            with open(self.db_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # 初始化空数据结构
        return {
            'suppliers': [],
            'code_history': [],
            'config': {
                'admin_password': self._hash_password('admin123'),
                'schedule_cron': '0 0 * * 1',
                'schedule_desc': '每周一 00:00'
            },
            'audit_log': []
        }
    
    def _save(self):
        """保存数据"""
        with open(self.db_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def _hash_password(self, password):
        """SHA256 哈希密码"""
        import hashlib
        return hashlib.sha256(password.encode()).hexdigest()
    
    # Suppliers
    def get_suppliers(self, active_only=True):
        """获取厂家列表"""
        suppliers = self.data['suppliers']
        if active_only:
            return [s for s in suppliers if s.get('is_active', True)]
        return suppliers
    
    def add_supplier(self, name):
        """添加厂家"""
        supplier_id = max([s['id'] for s in self.data['suppliers']], default=0) + 1
        supplier = {
            'id': supplier_id,
            'name': name,
            'is_active': True,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.data['suppliers'].append(supplier)
        self._save()
        return supplier
    
    def delete_supplier(self, supplier_id):
        """删除厂家（软删除）"""
        for supplier in self.data['suppliers']:
            if supplier['id'] == supplier_id:
                supplier['is_active'] = False
                supplier['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self._save()
                return True
        return False
    
    def restore_supplier(self, supplier_id):
        """恢复厂家"""
        for supplier in self.data['suppliers']:
            if supplier['id'] == supplier_id:
                supplier['is_active'] = True
                supplier['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self._save()
                return True
        return False
    
    # Code History
    def get_code_history(self, limit=100):
        """获取编码历史"""
        history = self.data['code_history']
        # 按时间倒序
        history.sort(key=lambda x: x['generated_at'], reverse=True)
        return history[:limit]
    
    def get_codes_by_week(self, year, week):
        """获取指定周的编码"""
        return [
            h for h in self.data['code_history']
            if h['year'] == year and h['week_number'] == week
        ]
    
    def save_codes(self, year, week, codes_dict):
        """保存编码"""
        # 删除该周的旧记录
        self.data['code_history'] = [
            h for h in self.data['code_history']
            if not (h['year'] == year and h['week_number'] == week)
        ]
        
        # 添加新记录
        generated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for supplier_name, code in codes_dict.items():
            record = {
                'id': len(self.data['code_history']) + 1,
                'year': year,
                'week_number': week,
                'supplier_name': supplier_name,
                'code': code,
                'generated_at': generated_at
            }
            self.data['code_history'].append(record)
        
        self._save()
    
    # Config
    def get_config(self):
        """获取配置"""
        return self.data['config']
    
    def update_config(self, key, value):
        """更新配置"""
        self.data['config'][key] = value
        self._save()
    
    # Audit Log
    def add_log(self, operation, details):
        """添加日志"""
        log = {
            'id': len(self.data['audit_log']) + 1,
            'operation': operation,
            'details': details,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.data['audit_log'].append(log)
        self._save()
    
    def get_logs(self, limit=100):
        """获取日志"""
        logs = self.data['audit_log']
        logs.sort(key=lambda x: x['timestamp'], reverse=True)
        return logs[:limit]


# 全局数据库实例
db = JSONDatabase()


def init_database():
    """初始化数据库"""
    # 检查是否需要初始化
    if not db.data['suppliers']:
        # 初始化36家厂家
        initial_suppliers = [
            '荣信化工', '兖矿荣信化工', '山东兖矿国宏化工', '滕州市天科化工',
            '四川金象赛瑞', '陕西富德化工', '内蒙古博大实地化学',
            '蒙大新能源化工', '兖州煤业榆林能化', '神木能源', '利源化学',
            '陕西黑猫化工', '云南云维股份', '六盘水化工', '安阳龙翔',
            '贵州赤天化股份', '兰炭能源', '上海宝丰', '鑫磊能源',
            '中煤鄂尔多斯', '内蒙古久泰能源', '内蒙兄弟甲醇', '神木天元化工',
            '陕西北元化工', '榆能化学', '乌海君正能源化工', '准格尔旗宏源化工',
            '新疆广汇新能源', '金虎化工', '山东铁雄能源', '冀中能源',
            '河北中海化工', '中煤河北', '陕西秦晋化工', '神木化学', '巨能新能源'
        ]
        
        for name in initial_suppliers:
            db.add_supplier(name)
        
        print('[数据库] 已初始化36家厂家')
```

---

### 6. 前端模板示例

#### 基础模板（templates/base.html）

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}精甲醇厂家周编码系统{% endblock %}</title>
    
    <!-- Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    
    <!-- Bootstrap Icons -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css" rel="stylesheet">
    
    <!-- 自定义样式 -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/industrial.css') }}">
    
    {% block extra_css %}{% endblock %}
</head>
<body class="industrial-theme">
    <!-- 导航栏 -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-industrial">
        <div class="container-fluid">
            <a class="navbar-brand" href="/">
                <i class="bi bi-diagram-3"></i>
                精甲醇厂家周编码系统
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="/">
                            <i class="bi bi-house"></i> 首页
                        </a>
                    </li>
                    {% if session.get('authenticated') %}
                    <li class="nav-item">
                        <a class="nav-link" href="/admin/dashboard">
                            <i class="bi bi-speedometer2"></i> 管理后台
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/auth/logout">
                            <i class="bi bi-box-arrow-right"></i> 退出
                        </a>
                    </li>
                    {% else %}
                    <li class="nav-item">
                        <a class="nav-link" href="/auth/login">
                            <i class="bi bi-lock"></i> 管理登录
                        </a>
                    </li>
                    {% endif %}
                </ul>
            </div>
        </div>
    </nav>
    
    <!-- 主内容 -->
    <div class="container mt-4">
        {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            {% for category, message in messages %}
            <div class="alert alert-{{ category }} alert-dismissible fade show" role="alert">
                {{ message }}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
            {% endfor %}
        {% endif %}
        {% endwith %}
        
        {% block content %}{% endblock %}
    </div>
    
    <!-- 页脚 -->
    <footer class="footer mt-5 py-3 bg-industrial text-center">
        <div class="container">
            <span class="text-muted">
                精甲醇厂家周编码系统 v1.0.0 | Python + Flask | 
                © 2026
            </span>
        </div>
    </footer>
    
    <!-- Bootstrap 5 JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    
    <!-- 自定义脚本 -->
    {% block extra_js %}{% endblock %}
</body>
</html>
```

#### 首页模板（templates/index.html）

```html
{% extends "base.html" %}

{% block title %}首页 - 精甲醇厂家周编码系统{% endblock %}

{% block content %}
<div class="row">
    <div class="col-12">
        <div class="card industrial-card mb-4">
            <div class="card-header">
                <h4 class="mb-0">
                    <i class="bi bi-calendar-week text-warning"></i>
                    本周编码 - {{ year }}年第{{ week }}周
                </h4>
            </div>
            <div class="card-body">
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <div>
                        <p class="mb-1">
                            <i class="bi bi-building"></i>
                            厂家数量：<strong>{{ codes|length }}</strong>
                        </p>
                        <p class="mb-0 text-muted">
                            <i class="bi bi-clock"></i>
                            生成时间：{{ generated_at or '未生成' }}
                        </p>
                    </div>
                    <div class="btn-group">
                        <button class="btn btn-warning" onclick="generateCodes()">
                            <i class="bi bi-arrow-clockwise"></i>
                            生成编码
                        </button>
                        <button class="btn btn-success" onclick="exportCodes()" {% if not codes %}disabled{% endif %}>
                            <i class="bi bi-download"></i>
                            导出
                        </button>
                        <button class="btn btn-secondary" onclick="location.reload()">
                            <i class="bi bi-arrow-repeat"></i>
                            刷新
                        </button>
                    </div>
                </div>
                
                {% if codes %}
                <div class="table-responsive">
                    <table class="table table-hover table-industrial">
                        <thead>
                            <tr>
                                <th style="width: 80px;">序号</th>
                                <th>厂家名称</th>
                                <th style="width: 120px;">编码</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for code in codes %}
                            <tr>
                                <td>{{ loop.index }}</td>
                                <td>{{ code.supplier }}</td>
                                <td>
                                    <span class="code-badge">{{ code.code }}</span>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
                {% else %}
                <div class="alert alert-info text-center">
                    <i class="bi bi-info-circle"></i>
                    本周尚未生成编码，请点击"生成编码"按钮
                </div>
                {% endif %}
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
function generateCodes() {
    if (!confirm('确定要生成本周编码吗？\n如果本周已有编码，将会被覆盖。')) {
        return;
    }
    
    fetch('/api/codes/generate', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'}
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            alert('生成成功！');
            location.reload();
        } else {
            alert('生成失败：' + data.message);
        }
    })
    .catch(err => {
        alert('请求失败：' + err);
    });
}

function exportCodes() {
    window.location.href = '/api/codes/export?year={{ year }}&week={{ week }}';
}
</script>
{% endblock %}
```

---

## 🎨 工业风格CSS（static/css/industrial.css）

```css
/* 煤化工工业风格主题 */

:root {
    /* 主色调 */
    --primary-dark: #1a2332;
    --primary-blue: #2c3e50;
    
    /* 强调色 */
    --accent-orange: #ff6b35;
    
    /* 辅助色 */
    --border-steel: #7f8c8d;
    --text-light: #ecf0f1;
    --text-secondary: #95a5a6;
    
    /* 功能色 */
    --success-green: #27ae60;
    --danger-red: #e74c3c;
}

/* 页面主题 */
body.industrial-theme {
    background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary-blue) 100%);
    min-height: 100vh;
    color: var(--text-light);
}

/* 导航栏 */
.bg-industrial {
    background-color: var(--primary-dark) !important;
    border-bottom: 3px solid var(--accent-orange);
}

.navbar-brand {
    font-weight: bold;
    color: var(--accent-orange) !important;
}

/* 工业卡片 */
.industrial-card {
    background: rgba(44, 62, 80, 0.8);
    backdrop-filter: blur(10px);
    border-left: 4px solid var(--accent-orange);
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
}

.card-header {
    background: rgba(26, 35, 50, 0.9);
    border-bottom: 2px solid var(--border-steel);
}

/* 表格 */
.table-industrial {
    color: var(--text-light);
    background: transparent;
}

.table-industrial thead th {
    background: var(--primary-dark);
    border-bottom: 2px solid var(--accent-orange);
    color: var(--accent-orange);
}

.table-industrial tbody tr {
    background: rgba(26, 35, 50, 0.6);
}

.table-industrial tbody tr:hover {
    background: rgba(255, 107, 53, 0.1);
}

/* 编码徽章 */
.code-badge {
    display: inline-block;
    padding: 6px 16px;
    background: linear-gradient(135deg, var(--accent-orange), #e85d04);
    color: white;
    font-weight: bold;
    font-size: 18px;
    font-family: 'Consolas', 'Monaco', monospace;
    border-radius: 6px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

/* 按钮 */
.btn-warning {
    background-color: var(--accent-orange);
    border-color: var(--accent-orange);
}

.btn-warning:hover {
    background-color: #e85d04;
    border-color: #e85d04;
}

/* 页脚 */
.footer {
    background-color: var(--primary-dark);
    border-top: 2px solid var(--accent-orange);
}
```

---

## 📦 打包成 exe

### 1. 安装 PyInstaller

```bash
pip install pyinstaller
```

### 2. 创建打包脚本（打包exe.bat）

```batch
@echo off
chcp 65001 >nul
echo ========================================
echo 精甲醇周编码系统 - 打包工具
echo ========================================
echo.

echo [1/3] 安装依赖...
pip install -r requirements.txt

echo [2/3] 打包成 exe...
pyinstaller ^
    --onefile ^
    --windowed ^
    --name "精甲醇编码系统" ^
    --icon=static/images/logo.ico ^
    --add-data "templates;templates" ^
    --add-data "static;static" ^
    --add-data "data;data" ^
    app.py

echo [3/3] 清理临时文件...
rd /s /q build

echo.
echo ========================================
echo ✅ 打包完成！
echo ========================================
echo.
echo 输出文件: dist\精甲醇编码系统.exe
echo 文件大小: 约 30MB
echo.
echo 部署方法：
echo 1. 将 exe 文件复制到目标电脑
echo 2. 双击运行即可
echo 3. 浏览器访问 http://localhost:3000
echo.
pause
```

### 3. 执行打包

```bash
# 方式1：双击运行
双击：打包exe.bat

# 方式2：命令行
python -m PyInstaller --onefile --windowed app.py
```

### 4. 打包结果

```
dist/
└── 精甲醇编码系统.exe  (约 30MB)
```

**特点：**
- ✅ 单文件 exe
- ✅ 内置 Python 运行时
- ✅ 无需安装任何依赖
- ✅ 双击即可运行
- ✅ 启动速度快（1-2秒）

---

## 🚀 部署方案

### 方案1：exe 部署（推荐）

**适用场景：** 生产环境、无 Python 环境的电脑

**步骤：**
```bash
1. 使用 PyInstaller 打包成 exe
2. 将 exe 文件复制到生产电脑
3. 双击运行 exe
4. 浏览器访问 http://localhost:3000
```

**优点：**
- ✅ 零依赖，双击即用
- ✅ 文件体积小（~30MB）
- ✅ 启动快速
- ✅ 适合非技术人员

---

### 方案2：源码部署

**适用场景：** 开发环境、有 Python 的服务器

**步骤：**
```bash
# 1. 安装 Python 3.8+
python --version

# 2. 安装依赖
pip install -r requirements.txt

# 3. 初始化数据库
python -c "from models.database import init_database; init_database()"

# 4. 启动应用
python app.py

# 或使用 gunicorn（生产环境推荐）
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:3000 app:app
```

---

### 方案3：Docker 部署

**Dockerfile：**
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 3000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:3000", "app:app"]
```

**docker-compose.yml：**
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "3000:3000"
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    environment:
      - FLASK_ENV=production
    restart: unless-stopped
```

**启动：**
```bash
docker-compose up -d
```

---

## 🔧 完整依赖列表（requirements.txt）

```
# Web 框架
Flask==3.0.0
Flask-CORS==4.0.0

# 定时任务
APScheduler==3.10.4

# 认证
PyJWT==2.8.0

# 生产服务器（可选）
gunicorn==21.2.0

# 数据库（如果使用 SQLite）
# 无需额外依赖，Python 内置

# 打包工具（开发环境）
# pyinstaller==6.3.0
```

---

## 📊 功能对比：Python vs Node.js

| 功能模块 | Python 实现 | Node.js 实现 |
|----------|------------|-------------|
| **后端框架** | Flask (轻量) | Express (轻量) |
| **路由系统** | Blueprint | Router |
| **模板引擎** | Jinja2 | None (Vue SPA) |
| **前端框架** | Bootstrap 5 | Vue 3 + Element Plus |
| **数据存储** | JSON / SQLite | JSON |
| **认证方式** | Flask-Login + JWT | JWT |
| **定时任务** | APScheduler | node-cron |
| **打包部署** | PyInstaller (30MB) | 绿色版 (50MB) |
| **开发难度** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **部署难度** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **前端体验** | ⭐⭐⭐ 传统 | ⭐⭐⭐⭐⭐ 现代 |
| **学习曲线** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

---

## 🎯 选择建议

### 选择 Python 方案的理由：

✅ **打包超级简单** - PyInstaller 一行命令生成 exe  
✅ **文件体积更小** - ~30MB vs ~50MB  
✅ **Python 语法简洁** - 更容易维护  
✅ **适合后台脚本** - 定时任务、数据处理  
✅ **学习成本低** - 非前端开发者友好  

### 继续使用 Node.js 的理由：

✅ **Web UI 现代化** - Vue 3 + Element Plus 体验更好  
✅ **前端生态丰富** - npm 海量组件  
✅ **SPA 单页应用** - 无刷新切换，流畅  
✅ **实时性更好** - WebSocket 原生支持  
✅ **已经完成开发** - 切换成本高  

---

## 🎉 总结

### Python 技术栈优势

1. **打包部署极简**
   ```bash
   pyinstaller --onefile app.py
   # 生成单个 exe，完美！
   ```

2. **代码简洁易懂**
   ```python
   @app.route('/api/codes/current')
   def get_current_codes():
       codes = db.get_codes_by_week(year, week)
       return jsonify(codes)
   ```

3. **零学习曲线**
   - Flask 文档完善
   - Bootstrap 开箱即用
   - Python 语法简单

4. **适合小型项目**
   - 快速开发
   - 易于维护
   - 部署简单

### 建议

**如果重新开始做这个项目：**
- 推荐使用 **Python + Flask**
- 原因：打包部署更简单，Python 更易学

**当前项目已用 Node.js 完成：**
- 建议继续使用 **Node.js + Vue 3**
- 原因：前端体验更好，已投入开发成本

**最佳实践：**
```
主系统（Web界面）: Node.js + Vue 3 ✅ (当前)
辅助脚本（数据处理）: Python (如有需要可补充)
```

---

## 📞 参考资源

### 官方文档
- Flask: https://flask.palletsprojects.com/
- Jinja2: https://jinja.palletsprojects.com/
- Bootstrap 5: https://getbootstrap.com/
- PyInstaller: https://pyinstaller.org/

### 学习资源
- Flask Mega-Tutorial: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
- Bootstrap 5 入门: https://www.runoob.com/bootstrap5/bootstrap5-tutorial.html

---

**文档版本**：v1.0.0  
**创建时间**：2026-09-09  
**适用场景**：为当前 Node.js 项目提供 Python 技术栈替代方案参考

---

## 🚀 快速启动（Python 版本）

如果你决定尝试 Python 版本，可以按以下步骤快速开始：

```bash
# 1. 创建虚拟环境
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# 2. 安装依赖
pip install Flask Flask-CORS APScheduler PyJWT

# 3. 创建项目结构
mkdir methanol-coding-python
cd methanol-coding-python

# 4. 复制本文档中的代码文件
# - app.py
# - config.py
# - models/database.py
# - utils/code_generator.py
# - templates/base.html
# - templates/index.html
# - static/css/industrial.css

# 5. 初始化数据库
python -c "from models.database import init_database; init_database()"

# 6. 运行应用
python app.py

# 7. 访问系统
# 浏览器打开 http://localhost:3000
```

---

**Happy Coding! 🎉**

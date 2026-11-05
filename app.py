"""
精甲醇厂家周编码系统
Flask 应用主入口
"""

from flask import Flask, render_template, jsonify, request, session, redirect, url_for, flash
from core.generator import CodeGenerator
from core.storage import Storage
from auth.password import PasswordAuth
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

storage = Storage()


# ========== 公开路由 ==========

@app.route('/')
def index():
    """首页 - 查看本周编码"""
    codes_data = storage.get_current_codes()

    now = datetime.now()
    current_year = now.year
    current_week = now.isocalendar()[1]

    if codes_data:
        # 转换为列表格式便于展示
        mapping = codes_data['mapping']
        codes_list = [
            {'index': i+1, 'supplier': sup, 'code': code}
            for i, (sup, code) in enumerate(mapping.items())
        ]

        return render_template('index.html',
                             year=codes_data['year'],
                             week=codes_data['week'],
                             date=codes_data['date'],
                             codes=codes_list,
                             total=len(codes_list))
    else:
        return render_template('index.html',
                             year=current_year,
                             week=current_week,
                             codes=None,
                             total=0)


@app.route('/history')
def history():
    """历史记录页面"""
    history_list = storage.get_history(limit=20)
    return render_template('history.html', history=history_list)


# ========== 管理路由 ==========

@app.route('/login', methods=['GET', 'POST'])
def login():
    """登录页面"""
    if request.method == 'POST':
        password = request.form.get('password')
        if PasswordAuth.verify(password):
            session['authenticated'] = True
            flash('登录成功！', 'success')
            return redirect(url_for('admin'))
        else:
            flash('密码错误！', 'danger')

    return render_template('login.html')


@app.route('/logout')
def logout():
    """退出登录"""
    session.pop('authenticated', None)
    flash('已退出登录', 'info')
    return redirect(url_for('index'))


@app.route('/admin')
def admin():
    """管理后台"""
    if not session.get('authenticated'):
        flash('请先登录', 'warning')
        return redirect(url_for('login'))

    suppliers = storage.load_suppliers()
    history_list = storage.get_history(limit=10)

    return render_template('admin.html',
                         suppliers=suppliers,
                         history=history_list,
                         total_suppliers=len(suppliers))


# ========== API 路由 ==========

@app.route('/api/generate', methods=['POST'])
def generate_codes():
    """生成编码 - API"""
    try:
        suppliers = storage.load_suppliers()
        if not suppliers:
            return jsonify({'success': False, 'message': '厂家列表为空，请先添加厂家'})

        codes_data = CodeGenerator.generate(suppliers)
        storage.save_codes(codes_data)

        return jsonify({
            'success': True,
            'message': f'成功生成 {codes_data["year"]}年第{codes_data["week"]}周编码',
            'data': codes_data
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/api/suppliers', methods=['GET'])
def get_suppliers():
    """获取厂家列表"""
    suppliers = storage.load_suppliers()
    return jsonify({'success': True, 'data': suppliers})


@app.route('/api/suppliers/add', methods=['POST'])
def add_supplier():
    """添加厂家"""
    if not session.get('authenticated'):
        return jsonify({'success': False, 'message': '未授权'}), 401

    data = request.get_json()
    name = data.get('name', '').strip()

    if not name:
        return jsonify({'success': False, 'message': '厂家名称不能为空'})

    suppliers = storage.load_suppliers()

    if name in suppliers:
        return jsonify({'success': False, 'message': '厂家已存在'})

    suppliers.append(name)
    storage.save_suppliers(suppliers)

    return jsonify({'success': True, 'message': f'成功添加厂家：{name}'})


@app.route('/api/suppliers/delete', methods=['POST'])
def delete_supplier():
    """删除厂家"""
    if not session.get('authenticated'):
        return jsonify({'success': False, 'message': '未授权'}), 401

    data = request.get_json()
    name = data.get('name', '').strip()

    suppliers = storage.load_suppliers()

    if name not in suppliers:
        return jsonify({'success': False, 'message': '厂家不存在'})

    suppliers.remove(name)
    storage.save_suppliers(suppliers)

    return jsonify({'success': True, 'message': f'成功删除厂家：{name}'})


@app.route('/api/password/change', methods=['POST'])
def change_password():
    """修改密码"""
    if not session.get('authenticated'):
        return jsonify({'success': False, 'message': '未授权'}), 401

    data = request.get_json()
    old_password = data.get('old_password', '')
    new_password = data.get('new_password', '')

    if not old_password or not new_password:
        return jsonify({'success': False, 'message': '密码不能为空'})

    if len(new_password) < 6:
        return jsonify({'success': False, 'message': '新密码长度至少6位'})

    if PasswordAuth.change_password(old_password, new_password):
        return jsonify({'success': True, 'message': '密码修改成功'})
    else:
        return jsonify({'success': False, 'message': '原密码错误'})


# ========== 错误处理 ==========

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


# ========== 启动应用 ==========

if __name__ == '__main__':
    # 初始化厂家列表
    if not storage.load_suppliers():
        initial_suppliers = [
            "荣信化工",
            "兖矿荣信化工",
            "内蒙古黄陶勒盖煤炭有限责任公司",
            "宁夏享昱通化工有限公司",
            "鄂尔多斯市昊华国泰化工有限公司",
            "神华巴彦淖尔能源有限公司",
            "国家能源集团宁煤公司煤制油化工",
            "中国石化长城能源化工（宁夏）有限公司",
            "濮阳市于硕化工",
            "新能能源有限公司",
            "陕西精益化工有限公司",
            "内蒙古庆华集团",
            "国家能源集团西来峰甲醇厂",
            "内蒙古黑猫煤化工有限公司",
            "陕西延长石油榆林凯越",
            "MTO甲醇青海煜腾东程能源有限公司",
            "兖州煤业榆林能化",
            "内蒙古中煤远兴能源化工有限公司",
            "宁夏畅亿清洁能源有限责任公司",
            "MTO甲醇-青海盐湖镁业",
            "新疆广汇",
            "沪蒙能源",
            "内蒙古东日新能源",
            "宁夏亿利源工贸有限公司",
            "鄂托克旗新航焦化有限公司",
            "内蒙古广聚新材料有限责任公司",
            "宁夏和宁化学有限公司",
            "新疆广江新能源有限公司",
            "内蒙古君正化工",
            "新疆天智辰业化工有限公司",
            "新疆新业能源化工有限责任公司",
            "阿拉善盟东海新能源",
            "新疆中泰新材料",
            "兖矿新疆煤化工有限公司",
            "宜昌兴和化工有限责任公司",
            "陕西海泰隆环保科技有限公司",
        ]
        storage.save_suppliers(initial_suppliers)
        print('[初始化] 已导入36家厂家')

    print('''
========================================
   精甲醇厂家周编码系统 v1.0.0
========================================

[OK] 系统已启动
[URL] 访问地址: http://localhost:3000
[PWD] 默认密码: admin123
[TIP] 按 Ctrl+C 停止服务

========================================
    ''')

    app.run(host='0.0.0.0', port=3000, debug=True)

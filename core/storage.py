"""
数据存储器 - JSON文件操作
职责：读写数据，不关心业务逻辑
"""

import json
import os
from pathlib import Path
from datetime import datetime


class Storage:
    """JSON 存储"""

    DATA_DIR = Path(__file__).parent.parent / 'data'

    def __init__(self):
        self.DATA_DIR.mkdir(exist_ok=True)

    def load_suppliers(self) -> list:
        """加载厂家列表"""
        file = self.DATA_DIR / 'suppliers.json'
        if file.exists():
            with open(file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def save_suppliers(self, suppliers: list):
        """保存厂家列表"""
        file = self.DATA_DIR / 'suppliers.json'
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(suppliers, f, ensure_ascii=False, indent=2)

    def save_codes(self, codes_data: dict):
        """保存编码历史"""
        file = self.DATA_DIR / 'codes_history.json'

        history = []
        if file.exists():
            with open(file, 'r', encoding='utf-8') as f:
                history = json.load(f)

        # 删除同周的旧记录
        history = [h for h in history
                  if not (h['year'] == codes_data['year'] and h['week'] == codes_data['week'])]

        history.append(codes_data)

        # 按时间倒序排列
        history.sort(key=lambda x: (x['year'], x['week']), reverse=True)

        with open(file, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)

    def get_current_codes(self) -> dict:
        """获取本周编码"""
        now = datetime.now()
        year, week = now.year, now.isocalendar()[1]

        file = self.DATA_DIR / 'codes_history.json'
        if not file.exists():
            return None

        with open(file, 'r', encoding='utf-8') as f:
            history = json.load(f)

        for record in history:
            if record['year'] == year and record['week'] == week:
                return record

        return None

    def get_history(self, limit: int = 10) -> list:
        """获取历史记录"""
        file = self.DATA_DIR / 'codes_history.json'
        if not file.exists():
            return []

        with open(file, 'r', encoding='utf-8') as f:
            history = json.load(f)

        # 按时间倒序
        history.sort(key=lambda x: (x['year'], x['week']), reverse=True)

        return history[:limit]

    def get_codes_by_week(self, year: int, week: int) -> dict:
        """获取指定周的编码"""
        file = self.DATA_DIR / 'codes_history.json'
        if not file.exists():
            return None

        with open(file, 'r', encoding='utf-8') as f:
            history = json.load(f)

        for record in history:
            if record['year'] == year and record['week'] == week:
                return record

        return None

"""
密码认证模块
"""

import hashlib
import json
from pathlib import Path


class PasswordAuth:
    """密码管理"""

    CONFIG_FILE = Path(__file__).parent.parent / 'data' / 'config.json'

    @staticmethod
    def hash_password(password: str) -> str:
        """SHA256 哈希"""
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def verify(password: str) -> bool:
        """验证密码"""
        if not PasswordAuth.CONFIG_FILE.exists():
            # 默认密码: admin123
            default_hash = PasswordAuth.hash_password('admin123')
            PasswordAuth._save_config({'password_hash': default_hash})

        with open(PasswordAuth.CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)

        input_hash = PasswordAuth.hash_password(password)
        return input_hash == config.get('password_hash')

    @staticmethod
    def change_password(old_password: str, new_password: str) -> bool:
        """修改密码"""
        if not PasswordAuth.verify(old_password):
            return False

        config = {'password_hash': PasswordAuth.hash_password(new_password)}
        PasswordAuth._save_config(config)
        return True

    @staticmethod
    def _save_config(config: dict):
        """保存配置"""
        PasswordAuth.CONFIG_FILE.parent.mkdir(exist_ok=True)
        with open(PasswordAuth.CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)

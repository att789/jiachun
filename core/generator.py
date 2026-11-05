"""
编码生成器 - 基于原有逻辑优化
职责：生成周编码，不关心存储和展示
"""

import random
import string
from datetime import datetime


class CodeGenerator:
    """编码生成器"""
    EXCLUDED = set('DIJLOUVZ')
    ALLOWED = [c for c in string.ascii_uppercase if c not in {'D','I','J','L','O','U','V','Z'}]

    @staticmethod
    def generate(suppliers: list) -> dict:
        """
        生成周编码

        Args:
            suppliers: 厂家列表 ['荣信化工', '兖矿荣信化工', ...]

        Returns:
            dict: {
                'year': 2026,
                'week': 36,
                'date': '2026-09-09',
                'mapping': {'荣信化工': 'A', ...}
            }
        """
        count = len(suppliers)

        if count == 0:
            raise ValueError('厂家列表为空')

        if count > 342:
            raise ValueError(f'厂家数量超出限制：{count} > 342')

        # 生成编码池
        codes = CodeGenerator._generate_code_pool(count)

        # Fisher-Yates 洗牌算法
        random.shuffle(codes)

        # 获取当前周数
        now = datetime.now()
        year = now.year
        week_number = now.isocalendar()[1]
        date_str = now.strftime('%Y-%m-%d')

        # 分配编码
        mapping = {suppliers[i]: codes[i] for i in range(count)}

        return {
            'year': year,
            'week': week_number,
            'date': date_str,
            'mapping': mapping
        }

    @staticmethod
    def _generate_code_pool(count: int) -> list:
        """
        生成编码池

        Args:
            count: 需要的编码数量

        Returns:
            list: 编码列表
        """
        letters = CodeGenerator.ALLOWED
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

    @staticmethod
    def validate_code(code: str) -> bool:
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
        allowed = CodeGenerator.ALLOWED
        return all(c in allowed for c in code)


# 测试代码
if __name__ == '__main__':
    test_suppliers = [
        '荣信化工', '兖矿荣信化工', '内蒙古黄陶勒盖煤炭有限责任公司',
        '宁夏享昱通化工有限公司', '鄂尔多斯市昊华国泰化工有限公司'
    ]

    result = CodeGenerator.generate(test_suppliers)

    print(f"生成的编码 - {result['year']}年第{result['week']}周")
    print(f"日期：{result['date']}")
    print("映射关系：")
    for name, code in result['mapping'].items():
        print(f"  {name} → {code}")

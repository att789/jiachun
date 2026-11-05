import random
import string
from datetime import datetime


def main():
    # 1. 动态厂家名单
    suppliers = ["荣信化工",
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

    # 2. 排除容易混淆的字母：D, I, J, L, O, U, V, Z
    excluded_letters = set('DIJLOUVZ')
    allowed_letters = [c for c in string.ascii_uppercase if c not in excluded_letters]

    # 3. 构造候选编码池
    single_codes = allowed_letters.copy()  # 18个单字母
    double_codes = [a + b for a in allowed_letters for b in allowed_letters]  # 324个双字母

    random.shuffle(single_codes)

    total_needed = len(suppliers)
    single_count = len(single_codes)

    # 4. 动态适配逻辑
    if total_needed <= single_count:
        selected_codes = single_codes[:total_needed]
    else:
        needed_doubles = total_needed - single_count
        sample_size = min(needed_doubles, len(double_codes))
        random_doubles = random.sample(double_codes, sample_size)
        selected_codes = single_codes + random_doubles

    # 5. 拼接排版文本（带周数校验）
    now = datetime.now()
    today_str = now.strftime('%Y-%m-%d')
    week_number = now.isocalendar()[1]
    year = now.year

    lines = [
        f"【{year}年第{week_number}周精甲醇厂家随机编码映射表】",
        f"更新时间：{today_str}",
        f"该对照编码仅第{week_number}周有效，过期失效！",
        "---------------------------------------"
    ]
    for idx, (sup, code) in enumerate(zip(suppliers, selected_codes), 1):
        lines.append(f"{idx:02d}. {sup}→【{code}】")

    result= "\n".join(lines)
    print(result)
    return result

if __name__ == "__main__":
    main()


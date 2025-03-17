import datetime
from datetime import datetime
from backend.models import db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from backend.models.RecordModel import Record

# from get_records_by_employee_id import get_records_by_employee_id

def calculate_work_days(employee_id):
    try:
        # 查询数据库，获取特定 employee_id 的记录
        # 这里假设您已经有一个适用的数据库查询函数，返回符合条件的记录列表
        # records = db.session.query(Record).order_by(Record.user_id == employee_id).all()
        count = db.session.query(Record).filter(Record.user_id == employee_id).count()
        # 提取日期信息并转换为日期对象
        # dates = [record['timestamp'] for record in records]
        # dates = [datetime.strptime(date.strftime('%Y-%m-%d'), '%Y-%m-%d').date() for date in dates]

        # 计算工作天数
        # work_days = len(set(dates))
        work_days = count

        return work_days
    
    except Exception as e:
        return str(e)

def calculate_monthly_bonus(cycles, max_capacities, machine_down_time, work_days, sick_days, total_cleanliness_amount, quality_complaints, months):
    try:
        efficiency_bonus = calculate_efficiency_bonus(cycles, max_capacities, machine_down_time, work_days)
        print(efficiency_bonus)
        health_bonus = calculate_health_bonus(sick_days, months)
        print(health_bonus)
        quality_bonus = calculate_quality_bonus(quality_complaints, months)
        print(quality_bonus)
        cleanliness_bonus = calculate_cleanliness_bonus(total_cleanliness_amount, months)
        print(cleanliness_bonus)
        
        total_bonus = efficiency_bonus + health_bonus + quality_bonus \
                       + cleanliness_bonus
        
        bonuses = {
            'efficiency_bonus': efficiency_bonus,
            'health_bonus': health_bonus,
            'quality_bonus': quality_bonus,
            'cleanliness_bonus': cleanliness_bonus,
        }
        
        return {
            'total_bonus': total_bonus,
            'bonuses': bonuses
        }
    
    except ValueError as e:
        return str(e)



def calculate_efficiency_bonus(cycles, max_capacities, machine_down_time, work_days):
    total_efficiency = 0
    for cycle, max_capacity,machine_down_time in zip(cycles, max_capacities, machine_down_time):
        total_production_time = cycle * 450 / max_capacity
        daily_production_time = 450 - machine_down_time
        efficiency = total_production_time / daily_production_time
        
        if efficiency > 1.0:
            raise ValueError("Efficiency cannot exceed 100%")
        
        total_efficiency += efficiency
    
    average_efficiency = total_efficiency / work_days
    efficiency_bonus = 220 * average_efficiency
    return efficiency_bonus

def calculate_health_bonus(sick_days, months):
    if sick_days <= 5:
        return 1200/months
    elif sick_days <= 10:
        return 1200/months
    elif sick_days <= 13:
        return 1200/months
    else:
        return 0

def calculate_quality_bonus(quality_complaints, months):
    max_penalty = 840
    penalty_per_complaint = 210

    total_penalty = min(quality_complaints * penalty_per_complaint, max_penalty)
    quality_bonus = max_penalty - total_penalty

    return quality_bonus/months


def calculate_cleanliness_bonus(total_cleanliness_amount, months):
    cleanliness_bonus = total_cleanliness_amount / months
    return cleanliness_bonus

# Example usage
# cycles = [27, 27, 27,27,27,27, 27,27]
# max_capacities = [27, 27, 27,27,27,27,27,27]
# machine_down_time = 0
# work_days = calculate_work_days('969')
# sick_days = 0
# quality_complaints = 0
# total_cleanliness_amount = 120
# months = 12
#
# bonus_info = calculate_monthly_bonus(cycles, max_capacities, machine_down_time, work_days, sick_days, quality_complaints, total_cleanliness_amount, months)
# print("monthly Bonus for 2024:", bonus_info['total_bonus'])
# print("Bonuses:")
# for key, value in bonus_info['bonuses'].items():
#     print(key + ":", value)
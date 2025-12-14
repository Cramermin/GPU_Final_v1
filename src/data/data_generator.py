# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_mock_prices(days=30, seed=42):
    """
    生成合规的模拟价格数据（基于您的GPU价格指数）
    :param days: 生成多少天的数据
    :param seed: 随机种子（确保可复现）
    :return: pandas DataFrame
    """
    np.random.seed(seed)
    
    # 1. 读取您的合规数据集
    data_dir = os.path.join(os.path.dirname(__file__), "../../data")
    cleaned_data_path = os.path.join(data_dir, "cleaned_gpu_prices.csv")
    
    if not os.path.exists(cleaned_data_path):
        print(f"❌ 数据文件不存在: {cleaned_data_path}")
        print("💡 请先运行 validate_data.py 创建所需文件")
        # 使用默认值继续
        base_price = 1029.0
        print("⚠️ 未找到数据集，使用默认RTX 4080价格 $1,029")
    else:
        try:
            # 明确指定编码和数据类型
            cleaned_data = pd.read_csv(
                cleaned_data_path, 
                encoding='utf-8',
                dtype={'Price': str}
            )
            print("✅ 成功加载合规数据集")
            
            # 2. 精确筛选RTX 4080（排除Super型号）
            rtx4080_rows = cleaned_data[
                cleaned_data["Product"].str.contains(r'RTX 4080(?!\s+Super)', case=False, regex=True, na=False)
            ]
            
            # 3. 获取基础价格
            if not rtx4080_rows.empty:
                # 从您的数据集中提取RTX 4080价格
                price_str = str(rtx4080_rows.iloc[0]["Price"]).strip()
                # 移除$符号和逗号
                price_str = price_str.replace('$', '').replace(',', '')
                base_price = float(price_str)
                print(f"📊 使用您的合规数据集: RTX 4080价格 = ${base_price:,.2f}")
            else:
                base_price = 1029.0  # RTX 4080标准价格（美元）
                print("⚠️ 未找到精确的RTX 4080数据，使用默认价格 $1,029")
        except Exception as e:
            print(f"❌ 读取数据集出错: {str(e)}")
            base_price = 1029.0
            print("⚠️ 使用默认RTX 4080价格 $1,029")

    # 4. 生成日期序列
    today = datetime.now()
    dates = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days-1, -1, -1)]
    
    # 5. 模拟价格波动
    prices = []
    current_price = base_price
    for date_str in dates:
        current_date = datetime.strptime(date_str, "%Y-%m-%d")
        # 大促日特殊处理
        if current_date.month == 6 and current_date.day == 18:
            current_price *= 0.92  # 618降价8%
        elif current_date.month == 11 and current_date.day == 11:
            current_price *= 0.88  # 双11降价12%
        else:
            # 日常波动：-1% ~ +1.5%
            daily_change = np.random.uniform(-0.01, 0.015)
            current_price *= (1 + daily_change)
        
        # 价格合理性校验（RTX 4080合理范围）
        current_price = max(850, min(current_price, 1200))
        prices.append(round(current_price, 2))
    
    # 6. 构建DataFrame
    df = pd.DataFrame({
        "date": dates,
        "rtx4080_price": prices,
        "data_source": "simulated"  # 标注为模拟数据
    })
    
    return df

def save_mock_data(output_path="data/historical_prices.csv"):
    """保存模拟数据到指定路径"""
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    df = generate_mock_prices()
    # 明确指定编码
    df.to_csv(output_path, index=False, encoding='utf-8')
    print(f"✅ 模拟数据已保存至: {output_path}")
    print(f"   数据范围: {df['date'].min()} 至 {df['date'].max()}")
    print(f"   价格范围: ${df['rtx4080_price'].min():,.2f} - ${df['rtx4080_price'].max():,.2f}")

if __name__ == "__main__":
    save_mock_data()
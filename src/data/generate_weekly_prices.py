# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_weekly_prices(days=7, seed=42):
    """
    为所有显卡生成一周的模拟价格数据
    :param days: 生成多少天的数据，默认为7天
    :param seed: 随机种子（确保可复现）
    :return: pandas DataFrame
    """
    np.random.seed(seed)
    
    # 1. 读取显卡基础价格数据
    data_dir = os.path.join(os.path.dirname(__file__), "../../data")
    cleaned_data_path = os.path.join(data_dir, "cleaned_gpu_prices.csv")
    
    try:
        # 读取显卡基础数据
        gpu_data = pd.read_csv(cleaned_data_path, encoding='utf-8')
        print(f"✅ 成功加载 {len(gpu_data)} 款显卡的基础价格数据")
    except Exception as e:
        print(f"❌ 读取显卡数据出错: {str(e)}")
        return None
    
    # 2. 生成日期序列（最近7天）
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days-1)
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # 3. 为每款显卡生成价格序列
    all_data = []
    
    for _, gpu in gpu_data.iterrows():
        product = gpu['Product']
        base_price = gpu['Price']
        
        # 如果价格是字符串，清理并转换为浮点数
        if isinstance(base_price, str):
            base_price = float(base_price.replace('$', '').replace(',', '').strip())
        elif pd.isna(base_price):
            # 如果价格缺失，使用同系列产品的平均价格
            series = product.split()[-1]
            similar_gpus = gpu_data[gpu_data['Product'].str.contains(series, regex=False)]
            base_price = similar_gpus['Price'].dropna().mean()
            if pd.isna(base_price):
                base_price = 500  # 默认基础价格
        
        # 为每款显卡生成7天价格
        prices = []
        current_price = base_price
        
        for _ in range(days):
            # 每日价格波动：-2% ~ +3%
            daily_change = np.random.uniform(-0.02, 0.03)
            current_price *= (1 + daily_change)
            
            # 确保价格合理（不低于历史最低价的90%）
            historical_low = gpu['Historical_Low']
            if not pd.isna(historical_low):
                if isinstance(historical_low, str):
                    historical_low = float(historical_low.replace('$', '').replace(',', '').strip())
                min_price = historical_low * 0.9
                current_price = max(min_price, current_price)
            
            prices.append(round(current_price, 2))
        
        # 添加到结果集
        for i, date in enumerate(date_range):
            all_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'product': product,
                'price': prices[i],
                'base_price': base_price
            })
    
    # 4. 创建DataFrame
    df = pd.DataFrame(all_data)
    
    # 5. 保存到文件
    output_path = os.path.join(data_dir, 'weekly_gpu_prices.csv')
    df.to_csv(output_path, index=False, encoding='utf-8')
    
    print(f"✅ 成功生成 {len(gpu_data)} 款显卡的 {days} 天价格数据")
    print(f"   数据已保存至: {output_path}")
    print(f"   时间范围: {start_date.strftime('%Y-%m-%d')} 至 {end_date.strftime('%Y-%m-%d')}")
    
    return df

if __name__ == "__main__":
    generate_weekly_prices(days=7)

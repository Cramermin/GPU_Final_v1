# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_weekly_prices():
    # 1. 读取显卡基础价格数据
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    input_file = os.path.join(data_dir, "cleaned_gpu_prices.csv")
    output_file = os.path.join(data_dir, "weekly_gpu_prices.csv")
    
    # 2. 读取基础价格数据
    gpu_data = pd.read_csv(input_file, encoding='utf-8')
    
    # 3. 生成日期序列（最近7天）
    end_date = datetime.now()
    start_date = end_date - timedelta(days=6)  # 总共7天
    dates = [(end_date - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
    
    # 4. 为每款显卡生成价格序列
    all_data = []
    
    for _, gpu in gpu_data.iterrows():
        product = gpu['Product']
        try:
            base_price = float(str(gpu['Price']).replace('$', '').replace(',', '').strip())
        except:
            base_price = 500  # 默认基础价格
            
        # 为每款显卡生成7天价格
        prices = []
        current_price = base_price
        
        for _ in range(7):
            # 每日价格波动：-2% ~ +3%
            daily_change = np.random.uniform(-0.02, 0.03)
            current_price *= (1 + daily_change)
            
            # 确保价格合理
            try:
                historical_low = float(str(gpu['Historical_Low']).replace('$', '').replace(',', '').strip())
                min_price = historical_low * 0.9
                current_price = max(min_price, current_price)
            except:
                pass
                
            prices.append(round(current_price, 2))
        
        # 添加到结果集
        for i, date in enumerate(dates):
            all_data.append({
                'date': date,
                'product': product,
                'price': prices[i],
                'base_price': round(base_price, 2)
            })
    
    # 5. 创建并保存DataFrame
    df = pd.DataFrame(all_data)
    df.to_csv(output_file, index=False, encoding='utf-8')
    
    print(f"已生成 {len(gpu_data)} 款显卡的7天价格数据")
    print(f"数据已保存至: {output_file}")
    return df

if __name__ == "__main__":
    generate_weekly_prices()

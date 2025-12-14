import pandas as pd
import json
from datetime import datetime, timedelta
import os

def convert_gpu_prices():
    # 读取CSV文件
    df = pd.read_csv('data/cleaned_gpu_prices.csv')
    
    # 转换数据格式
    gpu_prices = []
    for _, row in df.iterrows():
        try:
            price = float(str(row['Price']).replace('$', '').replace(',', '').strip())
            historical_low = float(str(row['Historical_Low']).replace('$', '').replace(',', '').strip()) \
                if pd.notna(row['Historical_Low']) and str(row['Historical_Low']).strip() != '' else price
            
            # 计算涨跌幅
            change = ((price - historical_low) / historical_low) * 100
            
            gpu_prices.append({
                'product': row['Product'],
                'price': price,
                'base_price': historical_low,
                'change': round(change, 2)
            })
        except Exception as e:
            print(f"处理 {row['Product']} 时出错: {e}")
    
    # 保存为JSON
    with open('gpu-price-site/data/gpu_prices.json', 'w', encoding='utf-8') as f:
        json.dump(gpu_prices, f, ensure_ascii=False, indent=2)
    
    print(f"已转换 {len(gpu_prices)} 个显卡价格数据")

def generate_price_history():
    # 生成12月8日至14日的历史价格数据
    gpu_data = pd.read_csv('data/cleaned_gpu_prices.csv')
    price_history = {}
    
    # 设置随机种子以确保结果可重现
    np.random.seed(42)
    
    for _, row in gpu_data.iterrows():
        product = row['Product']
        try:
            base_price = float(str(row['Price']).replace('$', '').replace(',', '').strip())
            prices = []
            
            # 为12月8日至14日生成价格数据
            # 12月8日（周一）到12月14日（周日）
            current_price = base_price
            
            # 生成7天的价格数据
            for day in range(7):
                # 工作日和周末的价格波动不同
                if day < 5:  # 周一到周五
                    # 工作日价格波动较小：-2% 到 +3%
                    change = 1 + (np.random.random() * 0.05 - 0.02)
                else:  # 周末
                    # 周末价格波动较大：-5% 到 +5%
                    change = 1 + (np.random.random() * 0.1 - 0.05)
                
                # 确保价格不会低于历史最低价的90%
                try:
                    historical_low = float(str(row['Historical_Low']).replace('$', '').replace(',', '').strip())
                    min_price = historical_low * 0.9
                    current_price = max(min_price, round(current_price * change, 2))
                except:
                    current_price = round(current_price * change, 2)
                
                prices.append(current_price)
            
            price_history[product] = prices
            
        except Exception as e:
            print(f"生成 {product} 历史价格时出错: {e}")
    
    # 保存为JSON
    with open('gpu-price-site/data/price_history.json', 'w', encoding='utf-8') as f:
        json.dump(price_history, f, ensure_ascii=False, indent=2)
    
    print(f"已生成 {len(price_history)} 个显卡的历史价格数据")

if __name__ == "__main__":
    import numpy as np
    
    # 确保输出目录存在
    os.makedirs('gpu-price-site/data', exist_ok=True)
    
    # 转换数据
    convert_gpu_prices()
    generate_price_history()

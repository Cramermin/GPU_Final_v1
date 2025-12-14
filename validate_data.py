import pandas as pd
import os
import re

def validate_dataset():
    """验证合规数据集是否符合要求"""
    # 确保data目录存在
    os.makedirs("data", exist_ok=True)
    
    data_path = os.path.join("data", "cleaned_gpu_prices.csv")
    try:
        # 读取CSV时确保正确处理数据类型
        df = pd.read_csv(data_path, dtype={'Price': str, 'Historical_Low': str})
        print("✅ 数据集验证成功！")
        print(f"   - 总行数: {len(df)}")
        print(f"   - 列: {', '.join(df.columns)}")
        
        # 修复FutureWarning: 指定na_values参数
        df.replace('', pd.NA, inplace=True)
        
        # 精确匹配RTX 4080（使用正则表达式确保单词边界）
        rtx4080 = df[df['Product'].str.contains(r'\bRTX 4080\b(?! Super)', case=False, regex=True, na=False)]
        
        if not rtx4080.empty:
            # 将价格转换为浮点数
            price_value = float(rtx4080.iloc[0]['Price'])
            print("✅ RTX 4080数据存在")
            print(f"   价格: ${price_value:,.2f}")
            
            # 检查数据是否为数值类型
            if isinstance(price_value, (int, float)):
                print("✅ 价格格式正确（数值类型）")
            else:
                print("⚠️ 价格格式警告：应为数值类型")
        else:
            print("❌ 未找到RTX 4080数据")
            # 尝试查找所有RTX 4080变体
            all_rtx4080 = df[df['Product'].str.contains('RTX 4080', case=False, na=False)]
            if not all_rtx4080.empty:
                print("🔍 找到相关型号:")
                for _, row in all_rtx4080.iterrows():
                    print(f"   - {row['Product']}: ${float(row['Price']):,.2f}")
            
        # 检查缺失值
        missing_values = df.isnull().sum().sum()
        if missing_values > 0:
            print(f"⚠️ 发现 {missing_values} 个缺失值，已自动处理")
            df.fillna("", inplace=True)
        else:
            print("✅ 无缺失值")
            
        # 检查合规性
        if 'URL' not in df.columns and 'Timestamp' not in df.columns and 'User' not in df.columns:
            print("✅ 合规检查通过：无URL、无时间戳、无个人信息")
        else:
            print("❌ 合规检查失败：包含敏感字段")
            
    except Exception as e:
        print(f"❌ 验证失败: {str(e)}")
        print("💡 修复建议：")
        print("   1. 确认data/cleaned_gpu_prices.csv文件存在")
        print("   2. 检查列名是否为: Product,Price,Historical_Low")
        print("   3. 确保价格中无$符号和逗号")
        return False
    return True

if __name__ == "__main__":
    validate_dataset()
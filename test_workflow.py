# -*- coding: utf-8 -*-
import sys
import io

# 设置标准输出编码为UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from src.core.workflow import PriceMonitorWorkflow
from src.core.ai_engine import BaseAIEngine

def main():
    print("\n" + "="*50)
    print("[TEST] 测试价格监控工作流 (无AI增强)")
    print("="*50 + "\n")

    try:
        # 1. 初始化工作流
        workflow = PriceMonitorWorkflow()
        workflow.set_ai_engine(BaseAIEngine())  # 使用基础AI引擎

        # 2. 运行工作流
        result = workflow.run_full_workflow()
        
        # 3. 打印结果
        if result.get('success', False):
            print("\n" + "="*50)
            print("[SUCCESS] 测试成功完成！")
            print(f"当前价格: ${result.get('current_price', 0):.2f}")
            if 'analysis' in result:
                print(f"趋势分析: {result['analysis'].get('trend', '未知')}")
                print(f"置信度: {result['analysis'].get('confidence', 0) * 100:.1f}%")
        else:
            print("\n" + "="*50)
            print("[WARNING] 测试完成，但数据不足")
            print(f"当前价格: ${result.get('current_price', 0):.2f}")
            print("请收集更多数据以获得完整分析")
            
    except Exception as e:
        print(f"\n[ERROR] 测试过程中出现错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    print("="*50)
    return 0

if __name__ == "__main__":
    sys.exit(main())
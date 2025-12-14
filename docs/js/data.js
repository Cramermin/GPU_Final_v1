// 模拟数据（当API不可用时使用）
function getMockData() {
    return [
        { 
            product: 'NVIDIA RTX 4090', 
            price: 15999, 
            base_price: 12999, 
            change: 23.1,
            history: [13999, 14499, 14999, 15499, 15799, 15999, 15999]
        },
        { 
            product: 'NVIDIA RTX 4080', 
            price: 8499, 
            base_price: 7999, 
            change: 6.3,
            history: [7999, 7999, 8099, 8199, 8299, 8399, 8499]
        },
        { 
            product: 'NVIDIA RTX 4070 Ti', 
            price: 6499, 
            base_price: 6499, 
            change: 0,
            history: [6499, 6499, 6499, 6499, 6499, 6499, 6499]
        },
        { 
            product: 'AMD RX 7900 XTX', 
            price: 7999, 
            base_price: 7999, 
            change: 0,
            history: [7999, 7999, 7999, 7999, 7999, 7999, 7999]
        },
        { 
            product: 'AMD RX 7900 XT', 
            price: 7399, 
            base_price: 7499, 
            change: -1.3,
            history: [7499, 7499, 7499, 7499, 7499, 7499, 7399]
        }
    ];
}

// 从CSV文件加载数据
async function loadGPUPrices() {
    try {
        // 在实际部署时，这里应该是一个API端点
        // 为了演示，我们使用模拟数据
        const response = await fetch('data/gpu_prices.json');
        if (!response.ok) {
            throw new Error('无法加载显卡价格数据');
        }
        return await response.json();
    } catch (error) {
        console.error('加载数据时出错:', error);
        // 返回模拟数据以防加载失败
        return getMockData();
    }
}

// 获取显卡的7天价格数据
async function getGPUPriceHistory(gpuName) {
    try {
        const response = await fetch('data/price_history.json');
        if (!response.ok) {
            throw new Error('无法加载历史价格数据');
        }
        const data = await response.json();
        return data[gpuName] || [];
    } catch (error) {
        console.error('加载历史数据时出错:', error);
        return [];
    }
}

// 获取购买建议
function getBuyingAdvice(currentPrice, basePrice, priceHistory) {
    if (!priceHistory || priceHistory.length < 2) {
        return { text: '数据不足', class: 'recommend-wait' };
    }
    
    const priceDiff = currentPrice - basePrice;
    const percentDiff = (priceDiff / basePrice) * 100;
    
    // 计算最近3天的平均价格
    const recentPrices = priceHistory.slice(-3);
    const avgRecentPrice = recentPrices.reduce((a, b) => a + b, 0) / recentPrices.length;
    
    if (currentPrice <= basePrice * 0.95) {
        return { text: '强烈推荐购买', class: 'recommend-buy' };
    } else if (currentPrice <= basePrice * 1.05 && currentPrice <= avgRecentPrice) {
        return { text: '推荐购买', class: 'recommend-buy' };
    } else if (currentPrice > basePrice * 1.1) {
        return { text: '不推荐购买', class: 'recommend-avoid' };
    } else {
        return { text: '建议观望', class: 'recommend-wait' };
    }
}

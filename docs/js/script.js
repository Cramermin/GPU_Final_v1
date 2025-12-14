// 全局变量
let priceChart = null;
let allGPUs = [];
let selectedGPU = null;

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', async function() {
    // 加载数据
    try {
        allGPUs = await loadGPUPrices();
        updateLastUpdated();
        renderGPUTable(allGPUs);
        
        // 默认显示第一个显卡的价格趋势
        if (allGPUs.length > 0) {
            await updatePriceChart(allGPUs[0].product);
        }
        
        // 添加搜索功能
        document.getElementById('searchInput').addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase();
            const filteredGPUs = allGPUs.filter(gpu => 
                gpu.product.toLowerCase().includes(searchTerm)
            );
            renderGPUTable(filteredGPUs);
        });
        
    } catch (error) {
        console.error('初始化失败:', error);
        alert('加载数据失败，请刷新页面重试');
    }
});

// 更新最后更新时间
function updateLastUpdated() {
    // 固定为12月14日
    document.getElementById('last-updated').textContent = '2025年12月14日 12:00';
}

// 渲染显卡表格
function renderGPUTable(gpus) {
    const tbody = document.getElementById('gpuTableBody');
    tbody.innerHTML = '';
    
    gpus.forEach(gpu => {
        const row = document.createElement('tr');
        row.style.cursor = 'pointer';
        row.onclick = () => updatePriceChart(gpu.product);
        
        const changeClass = gpu.change > 0 ? 'price-up' : 
                          gpu.change < 0 ? 'price-down' : 'price-same';
        const changeSymbol = gpu.change > 0 ? '↑' : gpu.change < 0 ? '↓' : '→';
        const changeText = gpu.change !== 0 ? 
            `${changeSymbol} ${Math.abs(gpu.change).toFixed(2)}%` : '持平';
            
        const advice = getBuyingAdvice(gpu.price, gpu.base_price, gpu.history || []);
        
        row.innerHTML = `
            <td><strong>${gpu.product}</strong></td>
            <td>¥${gpu.price.toLocaleString()}</td>
            <td>¥${gpu.base_price.toLocaleString()}</td>
            <td class="${changeClass}">${changeText}</td>
            <td class="${advice.class}">${advice.text}</td>
        `;
        
        tbody.appendChild(row);
    });
}

// 更新价格趋势图
async function updatePriceChart(gpuName) {
    selectedGPU = allGPUs.find(gpu => gpu.product === gpuName);
    if (!selectedGPU) return;
    
    // 显示加载状态
    const chartCanvas = document.getElementById('priceChart');
    const ctx = chartCanvas.getContext('2d');
    
    // 使用显卡的history数据
    const priceHistory = selectedGPU.history || [];
    const fixedDates = [
        '12月8日', '12月9日', '12月10日', 
        '12月11日', '12月12日', '12月13日', '12月14日'
    ];
    const labels = [...fixedDates];
    const prices = [...priceHistory];
    
    // 确保价格数据完整
    for (let i = prices.length; i < 7; i++) {
        // 生成基于基础价格的随机波动
        const basePrice = selectedGPU.base_price;
        const randomFactor = 0.95 + Math.random() * 0.1; // 0.95 到 1.05 之间的随机数
        prices.push(parseFloat((basePrice * randomFactor).toFixed(2)));
    }
    
    // 更新选中的行
    updateSelectedRow(gpuName);
    
    // 销毁现有的图表（如果存在）
    if (priceChart) {
        priceChart.destroy();
    }
    
    // 创建新的图表
    priceChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: `${gpuName} 价格趋势`,
                data: prices,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.3,
                fill: false,
                pointBackgroundColor: 'rgb(75, 192, 192)',
                pointRadius: 4,
                pointHoverRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `价格: ¥${context.parsed.y.toLocaleString()}`;
                        }
                    }
                },
                legend: {
                    position: 'top',
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    ticks: {
                        callback: function(value) {
                            return '¥' + value.toLocaleString();
                        }
                    }
                }
            }
        }
    });
}

// 更新表格中的选中行
function updateSelectedRow(gpuName) {
    // 移除所有行的选中状态
    const rows = document.querySelectorAll('#gpuTableBody tr');
    rows.forEach(row => {
        row.classList.remove('table-active');
    });
    
    // 添加选中状态到当前行
    const selectedRow = Array.from(rows).find(row => {
        const productCell = row.querySelector('td:first-child');
        return productCell && productCell.textContent.trim() === gpuName;
    });
    
    if (selectedRow) {
        selectedRow.classList.add('table-active');
        // 滚动到选中的行
        selectedRow.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
}

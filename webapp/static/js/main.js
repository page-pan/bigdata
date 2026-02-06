/**
 * 大数据智能分析系统 - 前端JavaScript
 */

document.addEventListener('DOMContentLoaded', function() {
    // 初始化
    initNavigation();
    loadSystemStatus();
    loadDatasets();
    loadTables();
    setupEventListeners();
});

// 导航切换
function initNavigation() {
    const navLinks = document.querySelectorAll('.nav-link[data-section]');
    const sections = document.querySelectorAll('.section');
    
    // 显示指定部分，隐藏其他部分
    function showSection(sectionId) {
        sections.forEach(section => {
            section.style.display = 'none';
        });
        
        const targetSection = document.getElementById(`${sectionId}-section`);
        if (targetSection) {
            targetSection.style.display = 'block';
        }
        
        // 更新导航链接状态
        navLinks.forEach(link => {
            if (link.getAttribute('data-section') === sectionId) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });
    }
    
    // 添加点击事件
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const sectionId = this.getAttribute('data-section');
            showSection(sectionId);
        });
    });
    
    // 默认显示仪表板
    showSection('dashboard');
}

// 加载系统状态
function loadSystemStatus() {
    fetch('/api/system/status')
        .then(response => response.json())
        .then(data => {
            updateStatusIndicator('hadoop', data.hadoop.namenode && data.hadoop.datanode);
            updateStatusIndicator('spark', data.spark.master && data.spark.worker);
            updateStatusIndicator('mysql', data.mysql);
            updateStatusIndicator('jupyter', data.jupyter);
            
            // 更新详细状态
            document.getElementById('namenode-status').textContent = 
                data.hadoop.namenode ? '运行中' : '停止';
            document.getElementById('datanode-status').textContent = 
                data.hadoop.datanode ? '运行中' : '停止';
            document.getElementById('spark-master-status').textContent = 
                data.spark.master ? '运行中' : '停止';
            document.getElementById('spark-worker-status').textContent = 
                data.spark.worker ? '运行中' : '停止';
            
            // 更新系统状态文本
            let statusText = '';
            if (data.hadoop.namenode && data.spark.master && data.mysql) {
                statusText = '所有系统运行正常';
            } else {
                statusText = '部分系统异常';
            }
            document.getElementById('system-status').innerHTML = 
                `<i class="bi bi-circle-fill text-success"></i> ${statusText}`;
        })
        .catch(error => {
            console.error('获取系统状态失败:', error);
            updateStatusIndicator('hadoop', false);
            updateStatusIndicator('spark', false);
            updateStatusIndicator('mysql', false);
            updateStatusIndicator('jupyter', false);
        });
}

function updateStatusIndicator(component, isUp) {
    const indicator = document.getElementById(`${component}-status`);
    const text = document.getElementById(`${component}-text`);
    
    if (indicator) {
        indicator.className = `status-indicator ${isUp ? 'status-up' : 'status-down'}`;
    }
    
    if (text) {
        text.textContent = isUp ? '运行正常' : '停止';
    }
}

// 数据集管理
function loadDatasets() {
    fetch('/api/datasets')
        .then(response => response.json())
        .then(data => {
            const datasetsList = document.getElementById('datasets-list');
            const datasetSelect = document.getElementById('dataset-select');
            
            datasetsList.innerHTML = '';
            datasetSelect.innerHTML = '<option value="">请选择数据集...</option>';
            
            if (data.datasets && data.datasets.length > 0) {
                data.datasets.forEach(dataset => {
                    // 添加到列表显示
                    const item = document.createElement('div');
                    item.className = 'dataset-item';
                    item.innerHTML = `
                        <div class="d-flex justify-content-between">
                            <div>
                                <strong>${dataset.name}</strong>
                                <span class="badge bg-${dataset.source === 'local' ? 'primary' : 'success'}">
                                    ${dataset.source}
                                </span>
                            </div>
                            <div>
                                <small class="text-muted">
                                    ${formatFileSize(dataset.size)} 
                                    ${dataset.records ? `| ${dataset.records} 条记录` : ''}
                                </small>
                            </div>
                        </div>
                    `;
                    datasetsList.appendChild(item);
                    
                    // 添加到下拉选择
                    const option = document.createElement('option');
                    option.value = dataset.name;
                    option.textContent = `${dataset.name} (${dataset.source})`;
                    datasetSelect.appendChild(option);
                });
            } else {
                datasetsList.innerHTML = '<p class="text-muted">暂无数据集</p>';
            }
        })
        .catch(error => {
            console.error('加载数据集失败:', error);
            document.getElementById('datasets-list').innerHTML = 
                '<p class="text-danger">加载数据集失败</p>';
        });
}

// 文件上传功能
function setupFileUpload() {
    const uploadArea = document.getElementById('upload-area');
    const fileInput = document.getElementById('file-input');
    
    // 点击上传区域触发文件选择
    uploadArea.addEventListener('click', function() {
        fileInput.click();
    });
    
    // 文件选择变化
    fileInput.addEventListener('change', function(e) {
        if (this.files.length > 0) {
            uploadFile(this.files[0]);
        }
    });
    
    // 拖放功能
    uploadArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        this.classList.add('dragover');
    });
    
    uploadArea.addEventListener('dragleave', function(e) {
        e.preventDefault();
        this.classList.remove('dragover');
    });
    
    uploadArea.addEventListener('drop', function(e) {
        e.preventDefault();
        this.classList.remove('dragover');
        
        if (e.dataTransfer.files.length > 0) {
            uploadFile(e.dataTransfer.files[0]);
        }
    });
}

function uploadFile(file) {
    if (!file.name.endsWith('.csv')) {
        alert('只支持CSV格式文件');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', file);
    
    const progressDiv = document.getElementById('upload-progress');
    const progressBar = progressDiv.querySelector('.progress-bar');
    const uploadStatus = document.getElementById('upload-status');
    
    progressDiv.style.display = 'block';
    progressBar.style.width = '0%';
    uploadStatus.textContent = '正在上传...';
    
    fetch('/api/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            progressBar.style.width = '100%';
            progressBar.classList.remove('progress-bar-animated');
            uploadStatus.textContent = '上传完成!';
            
            // 显示结果
            const resultDiv = document.getElementById('upload-result');
            resultDiv.innerHTML = `
                <div class="alert alert-success">
                    <i class="bi bi-check-circle"></i> ${data.message}
                    <br><small>HDFS路径: ${data.hdfs_path}</small>
                </div>
            `;
            resultDiv.style.display = 'block';
            
            // 重新加载数据集列表
            setTimeout(() => {
                loadDatasets();
                progressDiv.style.display = 'none';
                progressBar.classList.add('progress-bar-animated');
            }, 2000);
        } else {
            throw new Error(data.error || '上传失败');
        }
    })
    .catch(error => {
        console.error('上传失败:', error);
        progressDiv.style.display = 'none';
        alert(`上传失败: ${error.message}`);
    });
}

// Spark处理任务
function setupSparkProcessing() {
    const startBtn = document.getElementById('start-processing');
    
    startBtn.addEventListener('click', function() {
        const dataset = document.getElementById('dataset-select').value;
        const operation = document.getElementById('operation-select').value;
        
        if (!dataset) {
            alert('请选择数据集');
            return;
        }
        
        const processingResult = document.getElementById('processing-result');
        const processingMessage = document.getElementById('processing-message');
        const processingDetails = document.getElementById('processing-details');
        const sampleData = document.getElementById('sample-data');
        
        processingResult.style.display = 'block';
        processingMessage.textContent = '正在处理...';
        processingDetails.textContent = '';
        sampleData.innerHTML = '';
        
        startBtn.disabled = true;
        startBtn.innerHTML = '<i class="bi bi-hourglass-split"></i> 处理中...';
        
        fetch('/api/spark/process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                dataset: dataset,
                operation: operation
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                processingMessage.textContent = data.message;
                processingDetails.innerHTML = `
                    输出路径: ${data.output_path}<br>
                    处理行数: ${data.row_count}
                `;
                
                // 显示样本数据
                if (data.sample && data.sample.length > 0) {
                    let tableHtml = '<h6>样本数据:</h6><div class="table-responsive"><table class="table table-sm data-table"><thead><tr>';
                    
                    // 表头
                    const headers = Object.keys(data.sample[0]);
                    headers.forEach(header => {
                        tableHtml += `<th>${header}</th>`;
                    });
                    tableHtml += '</tr></thead><tbody>';
                    
                    // 数据行
                    data.sample.forEach(row => {
                        tableHtml += '<tr>';
                        headers.forEach(header => {
                            tableHtml += `<td>${row[header]}</td>`;
                        });
                        tableHtml += '</tr>';
                    });
                    
                    tableHtml += '</tbody></table></div>';
                    sampleData.innerHTML = tableHtml;
                }
                
                // 重新加载表列表
                loadTables();
            } else {
                throw new Error(data.error || '处理失败');
            }
        })
        .catch(error => {
            console.error('处理失败:', error);
            processingMessage.textContent = '处理失败';
            processingDetails.textContent = error.message;
        })
        .finally(() => {
            startBtn.disabled = false;
            startBtn.innerHTML = '<i class="bi bi-lightning-charge"></i> 开始处理';
        });
    });
}

// 可视化图表
function setupVisualization() {
    const generateBtn = document.getElementById('generate-chart');
    
    generateBtn.addEventListener('click', function() {
        const chartType = document.getElementById('chart-type').value;
        const dataTable = document.getElementById('data-table').value;
        
        fetch(`/api/visualization/data?table=${dataTable}&limit=50`)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    renderChart(chartType, data.data);
                } else {
                    throw new Error(data.error || '获取数据失败');
                }
            })
            .catch(error => {
                console.error('生成图表失败:', error);
                alert(`生成图表失败: ${error.message}`);
            });
    });
}

function renderChart(chartType, data) {
    const chartDom = document.getElementById('main-chart');
    const myChart = echarts.init(chartDom);
    
    let option;
    
    if (chartType === 'bar') {
        // 柱状图
        const xData = [];
        const yData = [];
        
        // 简单处理：使用前两个数值字段
        if (data.length > 0) {
            const keys = Object.keys(data[0]);
            const valueKey = keys.find(k => typeof data[0][k] === 'number' && k !== 'id');
            
            data.slice(0, 20).forEach(item => {
                const label = item[keys[0]] || '';
                xData.push(label);
                yData.push(item[valueKey] || 0);
            });
        }
        
        option = {
            title: {
                text: '数据统计柱状图',
                left: 'center'
            },
            tooltip: {
                trigger: 'axis'
            },
            xAxis: {
                type: 'category',
                data: xData,
                axisLabel: {
                    rotate: 45
                }
            },
            yAxis: {
                type: 'value'
            },
            series: [{
                data: yData,
                type: 'bar',
                itemStyle: {
                    color: '#1890ff'
                }
            }]
        };
    } else if (chartType === 'pie') {
        // 饼图
        const pieData = [];
        
        data.slice(0, 10).forEach((item, index) => {
            const keys = Object.keys(item);
            const valueKey = keys.find(k => typeof item[k] === 'number' && k !== 'id');
            
            if (valueKey) {
                pieData.push({
                    name: item[keys[0]] || `项目${index}`,
                    value: item[valueKey] || 0
                });
            }
        });
        
        option = {
            title: {
                text: '数据分布饼图',
                left: 'center'
            },
            tooltip: {
                trigger: 'item'
            },
            series: [{
                type: 'pie',
                radius: '60%',
                data: pieData,
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }]
        };
    } else if (chartType === 'line') {
        // 折线图
        const xData = [];
        const yData = [];
        
        data.slice(0, 20).forEach((item, index) => {
            const keys = Object.keys(item);
            const valueKey = keys.find(k => typeof item[k] === 'number' && k !== 'id');
            
            xData.push(index);
            yData.push(item[valueKey] || 0);
        });
        
        option = {
            title: {
                text: '数据趋势折线图',
                left: 'center'
            },
            tooltip: {
                trigger: 'axis'
            },
            xAxis: {
                type: 'category',
                data: xData
            },
            yAxis: {
                type: 'value'
            },
            series: [{
                data: yData,
                type: 'line',
                smooth: true,
                itemStyle: {
                    color: '#52c41a'
                }
            }]
        };
    }
    
    myChart.setOption(option);
    
    // 响应窗口大小变化
    window.addEventListener('resize', function() {
        myChart.resize();
    });
}

// 数据查询
function loadTables() {
    fetch('/api/mysql/tables')
        .then(response => response.json())
        .then(data => {
            const tablesList = document.getElementById('tables-list');
            const queryTableSelect = document.getElementById('query-table');
            
            tablesList.innerHTML = '';
            queryTableSelect.innerHTML = '<option value="">请选择表...</option>';
            
            if (data.tables && data.tables.length > 0) {
                data.tables.forEach(table => {
                    // 添加到列表显示
                    const item = document.createElement('div');
                    item.className = 'dataset-item';
                    item.innerHTML = `
                        <div>
                            <strong>${table}</strong>
                            <button class="btn btn-sm btn-outline-primary float-end" 
                                    onclick="queryTable('${table}')">
                                <i class="bi bi-search"></i> 查询
                            </button>
                        </div>
                    `;
                    tablesList.appendChild(item);
                    
                    // 添加到下拉选择
                    const option = document.createElement('option');
                    option.value = table;
                    option.textContent = table;
                    queryTableSelect.appendChild(option);
                });
                
                // 更新仪表板上的表数量
                document.getElementById('mysql-table-count').textContent = data.tables.length;
            } else {
                tablesList.innerHTML = '<p class="text-muted">暂无数据表</p>';
                document.getElementById('mysql-table-count').textContent = '0';
            }
        })
        .catch(error => {
            console.error('加载表列表失败:', error);
            document.getElementById('tables-list').innerHTML = 
                '<p class="text-danger">加载表列表失败</p>';
        });
}

function queryTable(tableName) {
    const limit = document.getElementById('row-limit').value || 50;
    
    fetch('/api/mysql/query', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            table: tableName,
            limit: limit
        })
    })
    .then(response => response.json())
    .then(data => {
        const queryResult = document.getElementById('query-result');
        
        if (data.success) {
            // 显示表结构
            let schemaHtml = '<h6>表结构:</h6><div class="table-responsive"><table class="table table-sm"><thead><tr><th>字段</th><th>类型</th><th>可空</th><th>键</th><th>默认值</th></tr></thead><tbody>';
            
            data.schema.forEach(field => {
                schemaHtml += `<tr>
                    <td>${field.Field}</td>
                    <td><code>${field.Type}</code></td>
                    <td>${field.Null}</td>
                    <td>${field.Key}</td>
                    <td>${field.Default || 'NULL'}</td>
                </tr>`;
            });
            
            schemaHtml += '</tbody></table></div>';
            
            // 显示数据
            let dataHtml = `<h6 class="mt-4">数据 (${data.count} 行):</h6><div class="table-responsive"><table class="table table-sm data-table"><thead><tr>`;
            
            if (data.data.length > 0) {
                const headers = Object.keys(data.data[0]);
                headers.forEach(header => {
                    dataHtml += `<th>${header}</th>`;
                });
                dataHtml += '</tr></thead><tbody>';
                
                data.data.forEach(row => {
                    dataHtml += '<tr>';
                    headers.forEach(header => {
                        const value = row[header];
                        dataHtml += `<td>${value !== null ? value : '<em>NULL</em>'}</td>`;
                    });
                    dataHtml += '</tr>';
                });
                
                dataHtml += '</tbody></table></div>';
            } else {
                dataHtml = '<p class="text-muted">表中暂无数据</p>';
            }
            
            queryResult.innerHTML = schemaHtml + dataHtml;
        } else {
            throw new Error(data.error || '查询失败');
        }
    })
    .catch(error => {
        console.error('查询失败:', error);
        document.getElementById('query-result').innerHTML = 
            `<div class="alert alert-danger">查询失败: ${error.message}</div>`;
    });
}

// 事件监听器设置
function setupEventListeners() {
    // 刷新数据集列表
    document.getElementById('refresh-datasets').addEventListener('click', loadDatasets);
    
    // 刷新表列表
    document.getElementById('refresh-tables').addEventListener('click', loadTables);
    
    // 执行查询按钮
    document.getElementById('execute-query').addEventListener('click', function() {
        const table = document.getElementById('query-table').value;
        if (table) {
            queryTable(table);
        } else {
            alert('请选择表');
        }
    });
    
    // 文件上传
    setupFileUpload();
    
    // Spark处理
    setupSparkProcessing();
    
    // 可视化
    setupVisualization();
    
    // 系统状态自动刷新
    setInterval(loadSystemStatus, 30000); // 每30秒刷新一次
}

// 工具函数
function formatFileSize(bytes) {
    if (bytes === 0) return '0 B';
    
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// 全局函数供按钮调用
window.queryTable = queryTable;
# 大数据教学演示系统

## 项目概述

本系统是一个面向教学演示的大数据处理平台，集成了Hadoop HDFS分布式存储、Spark分布式计算、MySQL关系型数据库和Jupyter Notebook交互式开发环境。系统提供了完整的数据处理流水线，支持数据上传、Spark处理、数据聚合、可视化展示等功能，适用于大数据课程的教学演示和学生实验。

## 系统架构

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web应用       │    │   Jupyter       │    │   Hadoop HDFS   │
│   (Flask)       │    │   Notebook      │    │   NameNode      │
│   Port: 5000    │    │   Port: 8888    │    │   Port: 9870    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────┬───────────┘                       │
                     │                                   │
             ┌───────┴───────┐                   ┌───────┴───────┐
             │   Spark集群   │                   │   Hadoop HDFS │
             │   Master      │                   │   DataNode    │
             │   Port: 7077  │                   │               │
             └───────────────┘                   └───────────────┘
                     │                                   │
                     └───────────┬───────────────────────┘
                                 │
                         ┌───────┴───────┐
                         │   MySQL数据库 │
                         │   Port: 3306  │
                         └───────────────┘
```

## 功能特性

### 1. 数据集管理
- 支持CSV格式数据集上传到HDFS
- 提供本地和HDFS数据集列表查看
- 数据集基本信息展示（大小、记录数）

### 2. Spark数据处理
- 电影评分数据分析（平均评分、评分次数）
- 电商交易数据分析（销售额、交易数量）
- 用户行为数据分析（会话时长、页面浏览）
- 日志数据分析（请求量、错误率、响应时间）

### 3. 数据聚合与存储
- 处理结果自动保存到HDFS
- 聚合数据存储到MySQL数据库
- 支持数据查询和导出

### 4. 可视化展示
- 使用ECharts生成交互式图表
- 支持柱状图、折线图、饼图等多种图表类型
- 实时数据可视化更新

### 5. Jupyter Notebook集成
- 预配置PySpark开发环境
- 提供示例Notebook
- 支持HDFS和MySQL访问

## 快速开始

### 环境要求
- Windows 11（已测试）
- Docker Desktop 4.0+
- 8GB+ 内存
- 20GB+ 可用磁盘空间

### 安装步骤

1. **克隆或下载项目**
   ```bash
   git clone <repository-url>
   cd bigdata
   ```

2. **生成数据集**
   ```bash
   python scripts/generate_datasets.py
   ```
   这将在`datasets/`目录下生成4个教学数据集：
   - `movies_metadata.csv` (100条电影元数据记录)
   - `ecommerce_transactions.csv` (60,000条电商交易记录)
   - `user_behavior.csv` (45,000条用户行为记录)
   - `log_analysis.csv` (55,000条日志记录)

3. **启动所有服务**
   ```bash
   docker-compose up -d
   ```
   这将启动以下服务：
   - Hadoop NameNode (端口: 9870)
   - Hadoop DataNode
   - Spark Master (端口: 8080)
   - Spark Worker (端口: 8081)
   - MySQL数据库 (端口: 3306)
   - Jupyter Notebook (端口: 8888)
   - Web应用 (端口: 5000)

4. **访问系统**
   - Web应用: http://localhost:5000
   - Jupyter Notebook: http://localhost:8888 (密码/Token: bigdata)
   - Hadoop NameNode UI: http://localhost:9870
   - Spark Master UI: http://localhost:8080

### 停止服务
```bash
docker-compose down
```

## 数据集说明

### 1. 电影元数据集 (movies_metadata.csv)
- **字段**: id, title, genre, year, rating, votes, director
- **记录数**: 100条
- **描述**: 电影元数据，包含电影标题、流派、年份、评分、投票数和导演信息

### 2. 电商交易数据集 (ecommerce_transactions.csv)
- **字段**: transaction_id, user_id, product_id, product_name, category, quantity, price, total_amount, timestamp
- **记录数**: 60,000条
- **描述**: 模拟电商平台交易数据，包含商品销售信息

### 3. 用户行为数据集 (user_behavior.csv)
- **字段**: session_id, user_id, session_duration_seconds, page_views, clicks, device_type, browser, timestamp
- **记录数**: 45,000条
- **描述**: 模拟网站用户行为数据，包含会话时长、页面浏览等信息

### 4. 日志分析数据集 (log_analysis.csv)
- **字段**: log_id, timestamp, endpoint, method, status_code, response_time_seconds, user_agent, ip_address
- **记录数**: 55,000条
- **描述**: 模拟Web服务器日志数据，包含请求、响应时间等信息

## Web应用使用指南

### 1. 仪表板
- 查看系统各组件运行状态
- 监控HDFS、Spark、MySQL服务状态
- 系统概览信息

### 2. 数据集管理
- **上传数据集**: 拖放或点击选择CSV文件上传到HDFS
- **查看数据集**: 列出所有可用数据集及其基本信息
- **刷新列表**: 更新数据集列表

### 3. 数据处理
- **选择数据集**: 从下拉菜单中选择要处理的数据集
- **选择操作**: 选择数据处理操作（数据聚合、筛选、转换）
- **开始处理**: 触发Spark处理任务，结果保存到HDFS和MySQL

### 4. 可视化展示
- **选择图表类型**: 柱状图、折线图、饼图、散点图
- **选择数据表**: 从MySQL聚合表中选择数据
- **生成图表**: 使用ECharts生成交互式可视化图表

### 5. 数据查询
- **选择表**: 从MySQL数据库表列表中选择
- **设置行数**: 设置查询结果返回的行数限制
- **执行查询**: 查看表结构和数据内容

## API接口

### 数据集管理
- `GET /api/datasets` - 获取数据集列表
- `POST /api/upload` - 上传文件到HDFS

### Spark处理
- `POST /api/spark/process` - 触发Spark处理任务
  ```json
  {
    "dataset": "movies_metadata.csv",
    "operation": "aggregate"
  }
  ```

### 数据查询
- `GET /api/mysql/tables` - 获取MySQL表列表
- `POST /api/mysql/query` - 执行MySQL查询
  ```json
  {
    "table": "movies_metadata",
    "limit": 100
  }
  ```

### 可视化数据
- `GET /api/visualization/data` - 获取可视化数据
  ```
  ?table=movies_metadata&limit=50
  ```

### 系统状态
- `GET /api/system/status` - 获取系统各组件状态

## Jupyter Notebook使用

### 访问地址
- URL: http://localhost:8888
- Token: `bigdata`

### 预安装包
- PySpark 3.5.6
- pandas, matplotlib, seaborn
- JupyterLab

### 示例Notebook
`notebooks/demo.ipynb` 包含以下内容：
1. Spark会话初始化
2. HDFS数据读取
3. 电影评分数据分析
4. 电商交易数据分析
5. MySQL数据库连接
6. 数据可视化
7. Spark SQL查询

### 运行Spark任务
```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("MyApp") \
    .config("spark.hadoop.fs.defaultFS", "hdfs://namenode:9000") \
    .getOrCreate()

# 读取HDFS数据
df = spark.read.csv("hdfs://namenode:9000/datasets/movies_metadata.csv", 
                   header=True, inferSchema=True)

# 数据处理
result = df.groupBy("genre").agg({"rating": "avg"})
result.show()
```

## 故障排除

### 常见问题

#### 1. 端口冲突
如果端口被占用，可以修改`docker-compose.yml`中的端口映射：
```yaml
ports:
  - "5001:5000"  # 修改外部端口
```

#### 2. Docker内存不足
- 增加Docker Desktop内存分配（建议8GB+）
- 停止不需要的容器

#### 3. 服务启动失败
检查服务日志：
```bash
docker-compose logs namenode
docker-compose logs spark-master
docker-compose logs mysql
```

#### 4. HDFS连接问题
确保NameNode服务已启动：
```bash
docker-compose ps | grep namenode
```

#### 5. Spark任务提交失败
检查Spark Master状态：
- 访问 http://localhost:8080
- 确保Worker节点已注册

### 日志查看
```bash
# 查看所有服务日志
docker-compose logs

# 查看特定服务日志
docker-compose logs webapp
docker-compose logs jupyter
```

## 教学应用场景

### 1. 大数据处理流程演示
- 数据采集 → 数据存储 → 数据处理 → 数据分析 → 数据可视化
- 展示完整的大数据处理生命周期

### 2. Hadoop HDFS教学
- HDFS架构和原理
- 文件系统的分布式存储
- 数据复制和容错机制

### 3. Spark编程教学
- RDD和DataFrame操作
- Spark SQL查询
- 分布式计算原理

### 4. 数据分析实践
- 数据清洗和预处理
- 统计分析和聚合计算
- 数据可视化技巧

### 5. 系统集成实践
- 多组件系统集成
- 服务间通信配置
- 容器化部署管理

## 项目结构

```
bigdata/
├── docker-compose.yml          # Docker Compose配置文件
├── README.md                   # 本文档
├── datasets/                   # 生成的数据集目录
│   ├── movies_metadata.csv
│   ├── ecommerce_transactions.csv
│   ├── user_behavior.csv
│   └── log_analysis.csv
├── docs/                       # 详细文档
├── hadoop-config/              # Hadoop配置文件
│   ├── core-site.xml
│   └── hdfs-site.xml
├── mysql-init/                 # MySQL初始化脚本
│   └── init.sql
├── notebooks/                  # Jupyter Notebook示例
│   └── demo.ipynb
├── scripts/                    # 数据处理脚本
│   ├── generate_datasets.py
│   └── spark_processor.py
├── spark-config/               # Spark配置文件
│   └── spark-defaults.conf
└── webapp/                     # Web应用
    ├── Dockerfile
    ├── requirements.txt
    ├── app.py
    ├── static/
    │   ├── css/style.css
    │   └── js/main.js
    └── templates/index.html
```

## 技术栈

### 基础设施
- **容器化**: Docker + Docker Compose
- **操作系统**: Windows 11 (兼容Linux/macOS)

### 大数据组件
- **分布式存储**: Hadoop HDFS 3.3.6
- **分布式计算**: Apache Spark 3.5.6
- **关系型数据库**: MySQL 8.0

### 开发框架
- **Web框架**: Flask (Python)
- **前端**: Bootstrap 5 + ECharts
- **开发环境**: Jupyter Notebook

### 编程语言
- **数据处理**: Python + PySpark
- **后端开发**: Python 3.9
- **前端开发**: HTML5 + JavaScript

## 开发与扩展

### 添加新数据集
1. 在`scripts/generate_datasets.py`中添加数据生成函数
2. 在`webapp/app.py`中添加对应的处理逻辑
3. 在MySQL初始化脚本中创建相应的表结构

### 添加新处理功能
1. 在`scripts/spark_processor.py`中添加处理函数
2. 在Web应用中添加相应的API端点
3. 更新前端界面

### 系统监控
- Hadoop NameNode UI: http://localhost:9870
- Spark Master UI: http://localhost:8080
- Spark Worker UI: http://localhost:8081
- MySQL监控: 可以使用MySQL Workbench连接

## 许可证

本项目采用 MIT 许可证。详见 LICENSE 文件。

## 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 联系与支持

如有问题或建议，请通过以下方式联系：
- 提交 GitHub Issue
- 发送电子邮件至 [示例邮箱]

## 更新日志

### v1.0.0 (2025-02-05)
- 初始版本发布
- 集成Hadoop HDFS、Spark、MySQL、Jupyter Notebook
- 提供完整的数据处理流水线
- 支持数据上传、处理、可视化功能

---

**注意**: 本系统为教学演示用途，生产环境需根据实际需求进行调整和优化。
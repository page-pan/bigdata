#!/usr/bin/env python3
"""
大数据教学演示系统 - Web应用
"""

import os
import json
import time
import subprocess
import requests
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import mysql.connector
import pandas as pd
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count, sum as spark_sum
import hdfs

app = Flask(__name__)
CORS(app)

# 配置
HDFS_NAMENODE = os.getenv('HDFS_NAMENODE', 'namenode:9000')
SPARK_MASTER = os.getenv('SPARK_MASTER', 'spark://spark-master:7077')
MYSQL_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'mysql'),
    'user': os.getenv('MYSQL_USER', 'demo'),
    'password': os.getenv('MYSQL_PASSWORD', 'demopassword'),
    'database': os.getenv('MYSQL_DATABASE', 'bigdata_demo')
}

# HDFS客户端
hdfs_client = hdfs.InsecureClient(f'http://{HDFS_NAMENODE.replace(":9000", ":9870")}')

# Spark会话（懒加载）
_spark_session = None

def get_spark_session():
    """获取或创建Spark会话"""
    global _spark_session
    if _spark_session is None:
        try:
            _spark_session = SparkSession.builder \
                .master(SPARK_MASTER) \
                .appName("BigDataDemo") \
                .config("spark.hadoop.fs.defaultFS", f"hdfs://{HDFS_NAMENODE}") \
                .getOrCreate()
            print(f"Spark会话已创建，连接到 {SPARK_MASTER}")
        except Exception as e:
            print(f"创建Spark会话失败: {e}")
            _spark_session = None
    return _spark_session

def get_mysql_connection():
    """获取MySQL连接"""
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        return conn
    except Exception as e:
        print(f"MySQL连接失败: {e}")
        return None

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/api/datasets')
def list_datasets():
    """列出可用数据集"""
    datasets = []
    local_dir = '/datasets'
    hdfs_dir = '/datasets'
    
    # 本地数据集
    if os.path.exists(local_dir):
        for file in os.listdir(local_dir):
            if file.endswith('.csv'):
                filepath = os.path.join(local_dir, file)
                size = os.path.getsize(filepath)
                datasets.append({
                    'name': file,
                    'source': 'local',
                    'size': size,
                    'records': estimate_records(filepath)
                })
    
    # HDFS数据集
    try:
        if hdfs_client.status(hdfs_dir, strict=False):
            for file_info in hdfs_client.list(hdfs_dir):
                if file_info['pathSuffix'].endswith('.csv'):
                    datasets.append({
                        'name': file_info['pathSuffix'],
                        'source': 'hdfs',
                        'size': file_info['length'],
                        'records': None
                    })
    except Exception as e:
        print(f"访问HDFS失败: {e}")
    
    return jsonify({'datasets': datasets})

def estimate_records(filepath):
    """估算CSV文件记录数"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            # 读取前几行估算
            lines = 0
            for i, line in enumerate(f):
                if i >= 10:
                    break
            if i > 0:
                # 估算总行数（减标题行）
                total_size = os.path.getsize(filepath)
                avg_line_size = total_size / (i + 1)
                return int(total_size / avg_line_size) - 1
    except:
        pass
    return None

@app.route('/api/upload', methods=['POST'])
def upload_to_hdfs():
    """上传文件到HDFS"""
    if 'file' not in request.files:
        return jsonify({'error': '没有文件'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '未选择文件'}), 400
    
    if not file.filename.endswith('.csv'):
        return jsonify({'error': '只支持CSV文件'}), 400
    
    try:
        # 保存到本地临时文件
        temp_path = f'/tmp/{file.filename}'
        file.save(temp_path)
        
        # 上传到HDFS
        hdfs_path = f'/datasets/{file.filename}'
        hdfs_client.upload(hdfs_path, temp_path)
        
        # 清理临时文件
        os.remove(temp_path)
        
        return jsonify({
            'success': True,
            'message': f'文件 {file.filename} 已上传到 HDFS',
            'hdfs_path': hdfs_path
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/spark/process', methods=['POST'])
def spark_process():
    """触发Spark处理任务"""
    data = request.json
    dataset_name = data.get('dataset')
    operation = data.get('operation', 'aggregate')
    
    if not dataset_name:
        return jsonify({'error': '未指定数据集'}), 400
    
    try:
        spark = get_spark_session()
        if spark is None:
            return jsonify({'error': 'Spark会话不可用'}), 500
        
        # 首先尝试从HDFS读取数据集
        hdfs_path = f'hdfs://{HDFS_NAMENODE}/datasets/{dataset_name}'
        local_path = f'/datasets/{dataset_name}'
        
        # 检查HDFS上是否存在文件
        try:
            hdfs_client.status(f'/datasets/{dataset_name}')
            df = spark.read.csv(hdfs_path, header=True, inferSchema=True)
            print(f"从HDFS读取: {hdfs_path}")
        except Exception as hdfs_error:
            # 如果HDFS上不存在，尝试从本地文件读取
            print(f"HDFS文件不存在: {hdfs_path}, 尝试本地文件: {local_path}")
            if os.path.exists(local_path):
                df = spark.read.csv(f'file://{local_path}', header=True, inferSchema=True)
                print(f"从本地文件读取: {local_path}")
                # 可选：将文件上传到HDFS供下次使用
                try:
                    hdfs_client.upload(f'/datasets/{dataset_name}', local_path)
                    print(f"文件已上传到HDFS: {dataset_name}")
                except Exception as upload_error:
                    print(f"文件上传到HDFS失败: {upload_error}")
            else:
                return jsonify({'error': f'数据集 {dataset_name} 在HDFS和本地都不存在'}), 400
        
        # 根据数据集和操作进行处理
        result_df = None
        output_path = None
        
        if dataset_name == 'movies_metadata.csv':
            if operation == 'aggregate':
                # 重命名列以匹配MySQL表结构
                result_df = df.select(
                    col('id').alias('movie_id'),
                    col('title'),
                    col('genre'),
                    col('year'),
                    col('rating'),
                    col('votes'),
                    col('director')
                )
                output_path = f'hdfs://{HDFS_NAMENODE}/results/movies_metadata_raw'
                
                # 保存到MySQL的movies_metadata表
                save_to_mysql(result_df, 'movies_metadata')
                
        elif dataset_name == 'ecommerce_transactions.csv':
            if operation == 'aggregate':
                result_df = df.groupBy('product_id', 'product_name', 'category') \
                    .agg(spark_sum('total_amount').alias('total_sales'),
                         count('transaction_id').alias('transaction_count'),
                         avg('price').alias('avg_price'))
                output_path = f'hdfs://{HDFS_NAMENODE}/results/ecommerce_agg'
                
                # 保存到MySQL
                save_to_mysql(result_df, 'ecommerce_transactions_agg')
        
        elif dataset_name == 'user_behavior.csv':
            if operation == 'aggregate':
                result_df = df.groupBy('user_id') \
                    .agg(count('session_id').alias('session_count'),
                         spark_sum('session_duration_seconds').alias('total_duration_seconds'),
                         avg('session_duration_seconds').alias('avg_session_duration'))
                output_path = f'hdfs://{HDFS_NAMENODE}/results/user_behavior_agg'
                
                # 保存到MySQL
                save_to_mysql(result_df, 'user_behavior_agg')
        
        elif dataset_name == 'log_analysis.csv':
            if operation == 'aggregate':
                from pyspark.sql.functions import hour
                result_df = df.withColumn('hour', hour('timestamp')) \
                    .groupBy('hour') \
                    .agg(count('log_id').alias('request_count'),
                         count(col('status_code') >= 400).alias('error_count'),
                         avg('response_time_seconds').alias('avg_response_time'))
                output_path = f'hdfs://{HDFS_NAMENODE}/results/log_analysis_agg'
                
                # 保存到MySQL
                save_to_mysql(result_df, 'log_analysis_agg')
        
        if result_df is not None and output_path is not None:
            # 保存处理结果到HDFS
            result_df.write.mode('overwrite').csv(output_path, header=True)
            
            # 收集结果样本用于返回
            sample = result_df.limit(10).toPandas().to_dict('records')
            
            return jsonify({
                'success': True,
                'message': f'数据集 {dataset_name} 处理完成',
                'output_path': output_path,
                'sample': sample,
                'row_count': result_df.count()
            })
        else:
            return jsonify({'error': '不支持的数据集或操作'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def save_to_mysql(spark_df, table_name):
    """将Spark DataFrame保存到MySQL"""
    try:
        # 转换为Pandas DataFrame
        pandas_df = spark_df.toPandas()
        
        # 获取MySQL连接
        conn = get_mysql_connection()
        if conn is None:
            return False
        
        cursor = conn.cursor()
        
        # 清空表
        cursor.execute(f"DELETE FROM {table_name}")
        
        # 插入数据
        for _, row in pandas_df.iterrows():
            columns = ', '.join(row.index)
            placeholders = ', '.join(['%s'] * len(row))
            sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            cursor.execute(sql, tuple(row))
        
        conn.commit()
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"保存到MySQL失败: {e}")
        return False

@app.route('/api/mysql/query', methods=['POST'])
def mysql_query():
    """执行MySQL查询"""
    data = request.json
    table_name = data.get('table')
    limit = data.get('limit', 100)
    
    if not table_name:
        return jsonify({'error': '未指定表名'}), 400
    
    try:
        conn = get_mysql_connection()
        if conn is None:
            return jsonify({'error': 'MySQL连接失败'}), 500
        
        cursor = conn.cursor(dictionary=True)
        
        # 获取表数据
        cursor.execute(f"SELECT * FROM {table_name} LIMIT {limit}")
        rows = cursor.fetchall()
        
        # 获取表结构
        cursor.execute(f"DESCRIBE {table_name}")
        schema = cursor.fetchall()
        
        # 递归转换bytes为字符串
        def convert_bytes(obj):
            if isinstance(obj, bytes):
                return obj.decode('utf-8', errors='replace')
            elif isinstance(obj, dict):
                return {k: convert_bytes(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_bytes(item) for item in obj]
            else:
                return obj
        
        rows = convert_bytes(rows)
        schema = convert_bytes(schema)
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'table': table_name,
            'schema': schema,
            'data': rows,
            'count': len(rows)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/mysql/tables')
def list_mysql_tables():
    """列出MySQL中的表"""
    try:
        conn = get_mysql_connection()
        if conn is None:
            return jsonify({'error': 'MySQL连接失败'}), 500
        
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = [row[0] for row in cursor.fetchall()]
        
        cursor.close()
        conn.close()
        
        return jsonify({'tables': tables})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/visualization/data')
def visualization_data():
    """获取可视化数据"""
    table_name = request.args.get('table', 'movies_metadata')
    limit = request.args.get('limit', 50)
    
    try:
        conn = get_mysql_connection()
        if conn is None:
            return jsonify({'error': 'MySQL连接失败'}), 500
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {table_name} LIMIT {limit}")
        rows = cursor.fetchall()
        
        # 递归转换bytes为字符串
        def convert_bytes(obj):
            if isinstance(obj, bytes):
                return obj.decode('utf-8', errors='replace')
            elif isinstance(obj, dict):
                return {k: convert_bytes(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_bytes(item) for item in obj]
            else:
                return obj
        
        rows = convert_bytes(rows)
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'table': table_name,
            'data': rows
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/system/status')
def system_status():
    """获取系统状态"""
    status = {
        'hadoop': {'namenode': False, 'datanode': False},
        'spark': {'master': False, 'worker': False},
        'mysql': False,
        'jupyter': False,
        'webapp': True
    }
    
    # 检查HDFS
    try:
        hdfs_client.status('/')
        status['hadoop']['namenode'] = True
        status['hadoop']['datanode'] = True
    except:
        pass
    
    # 检查Spark Master
    try:
        spark = get_spark_session()
        if spark is not None:
            status['spark']['master'] = True
            # 尝试通过Web UI检查Spark Worker
            response = requests.get('http://spark-master:8080', timeout=5)
            if response.status_code == 200:
                status['spark']['worker'] = True
    except:
        pass
    
    # 检查MySQL
    try:
        conn = get_mysql_connection()
        if conn is not None:
            status['mysql'] = True
            conn.close()
    except:
        pass
    
    # 检查Jupyter Notebook
    try:
        response = requests.get('http://jupyter-notebook:8888', timeout=5)
        if response.status_code == 200:
            status['jupyter'] = True
    except:
        pass
    
    return jsonify(status)

if __name__ == '__main__':
    # 确保HDFS目录存在
    try:
        hdfs_client.makedirs('/datasets')
        hdfs_client.makedirs('/results')
    except:
        pass
    
    app.run(host='0.0.0.0', port=5000, debug=True)
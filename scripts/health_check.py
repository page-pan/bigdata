#!/usr/bin/env python3
"""
系统健康检查脚本
检查各组件服务状态
"""

import requests
import mysql.connector
import hdfs
import time
import sys
from datetime import datetime

def check_hdfs():
    """检查HDFS服务"""
    try:
        client = hdfs.InsecureClient('http://localhost:9870')
        status = client.status('/')
        return True, f"HDFS NameNode运行正常 (容量: {status['capacity']} bytes)"
    except Exception as e:
        return False, f"HDFS连接失败: {e}"

def check_spark_master():
    """检查Spark Master服务"""
    try:
        response = requests.get('http://localhost:8080', timeout=10)
        if response.status_code == 200:
            return True, "Spark Master运行正常"
        else:
            return False, f"Spark Master返回状态码: {response.status_code}"
    except Exception as e:
        return False, f"Spark Master连接失败: {e}"

def check_mysql():
    """检查MySQL服务"""
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='demo',
            password='demopassword',
            database='bigdata_demo',
            port=3306
        )
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        cursor.close()
        conn.close()
        return True, f"MySQL运行正常 (表数量: {len(tables)})"
    except Exception as e:
        return False, f"MySQL连接失败: {e}"

def check_webapp():
    """检查Web应用服务"""
    try:
        response = requests.get('http://localhost:5000/api/system/status', timeout=10)
        if response.status_code == 200:
            data = response.json()
            return True, f"Web应用运行正常 (状态: {data})"
        else:
            return False, f"Web应用返回状态码: {response.status_code}"
    except Exception as e:
        return False, f"Web应用连接失败: {e}"

def check_jupyter():
    """检查Jupyter Notebook服务"""
    try:
        response = requests.get('http://localhost:8888', timeout=10)
        if response.status_code == 200:
            return True, "Jupyter Notebook运行正常"
        else:
            return False, f"Jupyter Notebook返回状态码: {response.status_code}"
    except Exception as e:
        return False, f"Jupyter Notebook连接失败: {e}"

def main():
    """主函数"""
    print("=" * 60)
    print("大数据教学演示系统 - 健康检查")
    print(f"检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    checks = [
        ("HDFS NameNode", check_hdfs),
        ("Spark Master", check_spark_master),
        ("MySQL数据库", check_mysql),
        ("Web应用", check_webapp),
        ("Jupyter Notebook", check_jupyter)
    ]
    
    all_passed = True
    results = []
    
    for name, check_func in checks:
        print(f"检查 {name}...", end=" ", flush=True)
        try:
            passed, message = check_func()
            if passed:
                print("✓")
                results.append(f"[PASS] {name}: {message}")
            else:
                print("✗")
                results.append(f"[FAIL] {name}: {message}")
                all_passed = False
        except Exception as e:
            print("✗")
            results.append(f"[ERROR] {name}: 检查异常 - {e}")
            all_passed = False
        
        time.sleep(1)
    
    print("\n" + "=" * 60)
    print("检查结果:")
    print("=" * 60)
    
    for result in results:
        print(result)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ 所有服务运行正常！")
        print("访问地址:")
        print("  Web应用: http://localhost:5000")
        print("  Jupyter Notebook: http://localhost:8888 (Token: bigdata)")
        print("  Hadoop UI: http://localhost:9870")
        print("  Spark UI: http://localhost:8080")
    else:
        print("✗ 部分服务存在问题，请检查日志。")
        print("运行以下命令查看服务日志:")
        print("  docker-compose logs")
    
    print("=" * 60)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
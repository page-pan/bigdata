#!/usr/bin/env python3
"""
大数据处理 - PySpark脚本
用于教学演示的Spark数据处理任务
"""

import sys
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count, sum as spark_sum, hour, when
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType, TimestampType

def create_spark_session(app_name="BigDataProcessor"):
    """创建Spark会话"""
    spark = SparkSession.builder \
        .appName(app_name) \
        .config("spark.hadoop.fs.defaultFS", "hdfs://namenode:9000") \
        .config("spark.sql.warehouse.dir", "hdfs://namenode:9000/user/hive/warehouse") \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel("WARN")
    return spark

def process_movies_metadata(spark, input_path, output_path):
    """处理电影元数据集"""
    print(f"处理电影元数据集: {input_path}")
    
    # 读取数据
    df = spark.read.csv(input_path, header=True, inferSchema=True)
    
    # 数据清洗
    df_clean = df.filter(col("rating").isNotNull() & (col("rating") >= 0) & (col("rating") <= 10))
    
    # 保存原始数据
    df_clean.write.mode("overwrite").csv(f"{output_path}/raw", header=True)
    
    # 1. 按导演统计
    director_stats = df_clean.groupBy("director") \
        .agg(
            avg("rating").alias("avg_rating"),
            count("id").alias("movie_count"),
            spark_sum("votes").alias("total_votes")
        ) \
        .orderBy(col("avg_rating").desc())
    
    # 2. 按流派统计
    genre_stats = df_clean.groupBy("genre") \
        .agg(
            avg("rating").alias("avg_rating"),
            count("id").alias("movie_count"),
            avg("votes").alias("avg_votes")
        ) \
        .orderBy(col("avg_rating").desc())
    
    # 3. 按年份统计
    year_stats = df_clean.groupBy("year") \
        .agg(
            avg("rating").alias("avg_rating"),
            count("id").alias("movie_count")
        ) \
        .orderBy("year")
    
    # 保存聚合结果
    director_stats.write.mode("overwrite").csv(f"{output_path}/director_stats", header=True)
    genre_stats.write.mode("overwrite").csv(f"{output_path}/genre_stats", header=True)
    year_stats.write.mode("overwrite").csv(f"{output_path}/year_stats", header=True)
    
    print(f"处理完成，结果保存到: {output_path}")
    print(f"总电影数: {df.count()}, 有效电影数: {df_clean.count()}")
    
    return df_clean

def process_ecommerce_transactions(spark, input_path, output_path):
    """处理电商交易数据集"""
    print(f"处理电商交易数据集: {input_path}")
    
    # 读取数据
    df = spark.read.csv(input_path, header=True, inferSchema=True)
    
    # 基本分析
    result = df.groupBy("product_id", "product_name", "category") \
        .agg(
            spark_sum("total_amount").alias("total_sales"),
            count("transaction_id").alias("transaction_count"),
            avg("price").alias("avg_price"),
            spark_sum("quantity").alias("total_quantity")
        ) \
        .orderBy(col("total_sales").desc())
    
    # 保存结果
    result.write.mode("overwrite").csv(output_path, header=True)
    
    print(f"处理完成，结果保存到: {output_path}")
    print(f"总交易额: {result.select(spark_sum('total_sales')).collect()[0][0]:.2f}")
    
    return result

def process_user_behavior(spark, input_path, output_path):
    """处理用户行为数据集"""
    print(f"处理用户行为数据集: {input_path}")
    
    # 读取数据
    df = spark.read.csv(input_path, header=True, inferSchema=True)
    
    # 用户分析
    user_stats = df.groupBy("user_id") \
        .agg(
            count("session_id").alias("session_count"),
            spark_sum("session_duration_seconds").alias("total_duration_seconds"),
            avg("session_duration_seconds").alias("avg_session_duration"),
            spark_sum("page_views").alias("total_page_views"),
            spark_sum("clicks").alias("total_clicks")
        ) \
        .withColumn("click_rate", col("total_clicks") / col("total_page_views")) \
        .orderBy(col("session_count").desc())
    
    # 设备分析
    device_stats = df.groupBy("device_type") \
        .agg(
            count("session_id").alias("session_count"),
            avg("session_duration_seconds").alias("avg_duration")
        )
    
    # 保存用户分析结果
    user_stats.write.mode("overwrite").csv(f"{output_path}/user_stats", header=True)
    device_stats.write.mode("overwrite").csv(f"{output_path}/device_stats", header=True)
    
    print(f"处理完成，结果保存到: {output_path}")
    print(f"总用户数: {user_stats.count()}")
    
    return user_stats

def process_log_analysis(spark, input_path, output_path):
    """处理日志分析数据集"""
    print(f"处理日志分析数据集: {input_path}")
    
    # 定义schema
    schema = StructType([
        StructField("log_id", IntegerType(), True),
        StructField("timestamp", TimestampType(), True),
        StructField("endpoint", StringType(), True),
        StructField("method", StringType(), True),
        StructField("status_code", IntegerType(), True),
        StructField("response_time_seconds", FloatType(), True),
        StructField("user_agent", StringType(), True),
        StructField("ip_address", StringType(), True)
    ])
    
    # 读取数据
    df = spark.read.csv(input_path, header=True, schema=schema)
    
    # 按小时分析
    hourly_stats = df.withColumn("hour", hour("timestamp")) \
        .groupBy("hour") \
        .agg(
            count("log_id").alias("request_count"),
            count(when(col("status_code") >= 400, 1)).alias("error_count"),
            avg("response_time_seconds").alias("avg_response_time"),
            count(when(col("status_code") == 200, 1)).alias("success_count")
        ) \
        .withColumn("error_rate", col("error_count") / col("request_count")) \
        .orderBy("hour")
    
    # 端点分析
    endpoint_stats = df.groupBy("endpoint", "method") \
        .agg(
            count("log_id").alias("request_count"),
            avg("response_time_seconds").alias("avg_response_time"),
            count(when(col("status_code") >= 400, 1)).alias("error_count")
        ) \
        .orderBy(col("request_count").desc())
    
    # 保存结果
    hourly_stats.write.mode("overwrite").csv(f"{output_path}/hourly_stats", header=True)
    endpoint_stats.write.mode("overwrite").csv(f"{output_path}/endpoint_stats", header=True)
    
    print(f"处理完成，结果保存到: {output_path}")
    print(f"总请求数: {df.count()}, 错误率: {hourly_stats.select(avg('error_rate')).collect()[0][0]:.2%}")
    
    return hourly_stats

def save_to_mysql(spark_df, table_name):
    """将Spark DataFrame保存到MySQL"""
    try:
        mysql_url = "jdbc:mysql://mysql:3306/bigdata_demo"
        mysql_properties = {
            "user": "demo",
            "password": "demopassword",
            "driver": "com.mysql.cj.jdbc.Driver"
        }
        
        spark_df.write \
            .mode("overwrite") \
            .jdbc(mysql_url, table_name, properties=mysql_properties)
        
        print(f"数据已保存到MySQL表: {table_name}")
        return True
    except Exception as e:
        print(f"保存到MySQL失败: {e}")
        return False

def main():
    """主函数"""
    if len(sys.argv) < 3:
        print("用法: python spark_processor.py <数据集类型> <输入路径> [输出路径]")
        print("数据集类型: movie, ecommerce, user, log")
        print("示例: python spark_processor.py movie hdfs://namenode:9000/datasets/movies_metadata.csv hdfs://namenode:9000/results")
        return
    
    dataset_type = sys.argv[1]
    input_path = sys.argv[2]
    output_path = sys.argv[3] if len(sys.argv) > 3 else f"hdfs://namenode:9000/results/{dataset_type}_output"
    
    # 创建Spark会话
    spark = create_spark_session(f"Processor-{dataset_type}")
    
    try:
        # 根据数据集类型选择处理函数
        if dataset_type == "movie":
            result = process_movies_metadata(spark, input_path, output_path)
            # 重命名id列为movie_id以匹配表结构
            result_for_mysql = result.select(
                col("id").alias("movie_id"),
                col("title"),
                col("genre"),
                col("year"),
                col("rating"),
                col("votes"),
                col("director")
            )
            # 保存到MySQL
            save_to_mysql(result_for_mysql, "movies_metadata")
            
        elif dataset_type == "ecommerce":
            result = process_ecommerce_transactions(spark, input_path, output_path)
            save_to_mysql(result, "ecommerce_transactions_agg")
            
        elif dataset_type == "user":
            result = process_user_behavior(spark, input_path, output_path)
            save_to_mysql(result.limit(100), "user_behavior_agg")  # 只保存前100行
            
        elif dataset_type == "log":
            result = process_log_analysis(spark, input_path, output_path)
            save_to_mysql(result, "log_analysis_agg")
            
        else:
            print(f"未知的数据集类型: {dataset_type}")
            return
        
        # 显示样本数据
        print("\n样本数据:")
        result.show(10)
        
        # 显示统计信息
        print("\n统计信息:")
        result.describe().show()
        
    except Exception as e:
        print(f"处理失败: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        # 停止Spark会话
        spark.stop()

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
生成教学用大数据集
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# 设置随机种子保证可重复性
np.random.seed(42)
random.seed(42)

def generate_movies_metadata(num_records=100):
    """生成电影元数据集"""
    print("生成电影元数据集...")
    
    # 示例电影数据，包含中文标题
    sample_movies = [
        {"id": 1, "title": "肖申克的救赎", "genre": "剧情", "year": 1994, "rating": 9.7, "votes": 2778477, "director": "弗兰克·德拉邦特"},
        {"id": 2, "title": "霸王别姬", "genre": "剧情/爱情", "year": 1993, "rating": 9.6, "votes": 1857493, "director": "陈凯歌"},
        {"id": 3, "title": "阿甘正传", "genre": "剧情/爱情", "year": 1994, "rating": 9.5, "votes": 2200000, "director": "罗伯特·泽米吉斯"},
        {"id": 4, "title": "这个杀手不太冷", "genre": "剧情/动作", "year": 1994, "rating": 9.4, "votes": 2100000, "director": "吕克·贝松"},
        {"id": 5, "title": "泰坦尼克号", "genre": "剧情/爱情", "year": 1997, "rating": 9.3, "votes": 2300000, "director": "詹姆斯·卡梅隆"},
        {"id": 6, "title": "盗梦空间", "genre": "科幻/悬疑", "year": 2010, "rating": 9.2, "votes": 2400000, "director": "克里斯托弗·诺兰"},
        {"id": 7, "title": "千与千寻", "genre": "动画/奇幻", "year": 2001, "rating": 9.1, "votes": 1900000, "director": "宫崎骏"},
        {"id": 8, "title": "辛德勒的名单", "genre": "剧情/历史", "year": 1993, "rating": 9.0, "votes": 1600000, "director": "史蒂文·斯皮尔伯格"},
        {"id": 9, "title": "星际穿越", "genre": "科幻/冒险", "year": 2014, "rating": 8.9, "votes": 1800000, "director": "克里斯托弗·诺兰"},
        {"id": 10, "title": "楚门的世界", "genre": "剧情/科幻", "year": 1998, "rating": 8.8, "votes": 1200000, "director": "彼得·威尔"}
    ]
    
    # 扩展更多电影
    genres = ["剧情", "喜剧", "动作", "爱情", "科幻", "恐怖", "动画", "悬疑", "犯罪", "奇幻"]
    directors = ["张艺谋", "李安", "王家卫", "诺兰", "斯皮尔伯格", "卡梅隆", "宫崎骏", "昆汀·塔伦蒂诺", "大卫·芬奇", "克里斯托弗·麦奎里"]
    
    data = []
    for i in range(num_records):
        if i < len(sample_movies):
            movie = sample_movies[i]
        else:
            # 生成更多电影数据
            movie_id = i + 1
            title = f"电影_{movie_id}"
            genre = random.choice(genres)
            year = random.randint(1980, 2023)
            rating = round(random.uniform(6.0, 9.9), 1)
            votes = random.randint(10000, 3000000)
            director = random.choice(directors)
            
            movie = {
                "id": movie_id,
                "title": title,
                "genre": genre,
                "year": year,
                "rating": rating,
                "votes": votes,
                "director": director
            }
        
        data.append(movie)
    
    df = pd.DataFrame(data)
    return df

def generate_ecommerce_transactions(num_records=60000):
    """生成电商交易数据集"""
    print("生成电商交易数据集...")
    
    products = [
        {'id': i, 'name': f'Product_{i}', 'category': random.choice(['Electronics', 'Clothing', 'Books', 'Home', 'Sports'])}
        for i in range(1, 201)
    ]
    
    data = []
    for i in range(num_records):
        product = random.choice(products)
        user_id = random.randint(1, 5000)
        quantity = random.randint(1, 5)
        price = round(random.uniform(10.0, 1000.0), 2)
        total = round(price * quantity, 2)
        timestamp = datetime.now() - timedelta(days=random.randint(0, 90))
        
        data.append({
            'transaction_id': i + 1,
            'user_id': user_id,
            'product_id': product['id'],
            'product_name': product['name'],
            'category': product['category'],
            'quantity': quantity,
            'price': price,
            'total_amount': total,
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    df = pd.DataFrame(data)
    return df

def generate_user_behavior(num_records=45000):
    """生成用户行为数据集"""
    print("生成用户行为数据集...")
    
    data = []
    for i in range(num_records):
        user_id = random.randint(1, 3000)
        session_duration = random.randint(30, 3600)
        page_views = random.randint(1, 50)
        clicks = random.randint(0, page_views)
        timestamp = datetime.now() - timedelta(days=random.randint(0, 30))
        
        data.append({
            'session_id': i + 1,
            'user_id': user_id,
            'session_duration_seconds': session_duration,
            'page_views': page_views,
            'clicks': clicks,
            'device_type': random.choice(['Mobile', 'Desktop', 'Tablet']),
            'browser': random.choice(['Chrome', 'Firefox', 'Safari', 'Edge']),
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    df = pd.DataFrame(data)
    return df

def generate_log_analysis(num_records=55000):
    """生成日志分析数据集"""
    print("生成日志分析数据集...")
    
    endpoints = ['/api/users', '/api/products', '/api/orders', '/api/auth', '/api/search']
    status_codes = [200, 201, 400, 401, 403, 404, 500]
    
    data = []
    for i in range(num_records):
        timestamp = datetime.now() - timedelta(seconds=random.randint(0, 86400*7))
        response_time = round(random.uniform(0.1, 2.0), 3)
        
        data.append({
            'log_id': i + 1,
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'endpoint': random.choice(endpoints),
            'method': random.choice(['GET', 'POST', 'PUT', 'DELETE']),
            'status_code': random.choice(status_codes),
            'response_time_seconds': response_time,
            'user_agent': random.choice(['Mozilla/5.0', 'curl/7.68.0', 'PostmanRuntime/7.26.8']),
            'ip_address': f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}'
        })
    
    df = pd.DataFrame(data)
    return df

def main():
    """主函数"""
    print("开始生成教学数据集...")
    
    # 生成数据集
    movies_metadata_df = generate_movies_metadata(100)
    ecommerce_df = generate_ecommerce_transactions(60000)
    user_behavior_df = generate_user_behavior(45000)
    log_df = generate_log_analysis(55000)
    
    # 保存为CSV文件
    output_dir = './datasets/'
    
    movies_metadata_df.to_csv(f'{output_dir}movies_metadata.csv', index=False)
    ecommerce_df.to_csv(f'{output_dir}ecommerce_transactions.csv', index=False)
    user_behavior_df.to_csv(f'{output_dir}user_behavior.csv', index=False)
    log_df.to_csv(f'{output_dir}log_analysis.csv', index=False)
    
    print(f"数据集已保存到 {output_dir}")
    print(f"电影元数据集: {len(movies_metadata_df)} 条记录")
    print(f"电商交易数据集: {len(ecommerce_df)} 条记录")
    print(f"用户行为数据集: {len(user_behavior_df)} 条记录")
    print(f"日志分析数据集: {len(log_df)} 条记录")

if __name__ == "__main__":
    main()
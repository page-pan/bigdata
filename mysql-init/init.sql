-- 创建聚合结果表
CREATE TABLE IF NOT EXISTS movie_ratings_agg (
    id INT AUTO_INCREMENT PRIMARY KEY,
    movie_id INT NOT NULL,
    title VARCHAR(255),
    genre VARCHAR(100),
    year INT,
    rating DECIMAL(3,1),
    votes INT,
    director VARCHAR(255),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS movies_metadata (
    id INT AUTO_INCREMENT PRIMARY KEY,
    movie_id INT NOT NULL,
    title VARCHAR(255),
    genre VARCHAR(100),
    year INT,
    rating DECIMAL(3,1),
    votes INT,
    director VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ecommerce_transactions_agg (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    product_name VARCHAR(255),
    total_sales DECIMAL(12,2),
    transaction_count INT,
    avg_price DECIMAL(10,2),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS user_behavior_agg (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    session_count INT,
    total_duration_seconds INT,
    avg_session_duration DECIMAL(10,2),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS log_analysis_agg (
    id INT AUTO_INCREMENT PRIMARY KEY,
    hour TIMESTAMP,
    request_count INT,
    error_count INT,
    avg_response_time DECIMAL(10,2),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 插入一些示例数据
INSERT INTO movie_ratings_agg (movie_id, title, genre, year, rating, votes, director) VALUES
(1, '肖申克的救赎', '剧情', 1994, 9.7, 2778477, '弗兰克·德拉邦特'),
(2, '霸王别姬', '剧情/爱情', 1993, 9.6, 1857493, '陈凯歌'),
(3, '阿甘正传', '剧情/爱情', 1994, 9.5, 2200000, '罗伯特·泽米吉斯'),
(4, '这个杀手不太冷', '剧情/动作', 1994, 9.4, 2100000, '吕克·贝松'),
(5, '泰坦尼克号', '剧情/爱情', 1997, 9.3, 2300000, '詹姆斯·卡梅隆'),
(6, '盗梦空间', '科幻/悬疑', 2010, 9.2, 2400000, '克里斯托弗·诺兰'),
(7, '千与千寻', '动画/奇幻', 2001, 9.1, 1900000, '宫崎骏'),
(8, '辛德勒的名单', '剧情/历史', 1993, 9.0, 1600000, '史蒂文·斯皮尔伯格'),
(9, '星际穿越', '科幻/冒险', 2014, 8.9, 1800000, '克里斯托弗·诺兰'),
(10, '楚门的世界', '剧情/科幻', 1998, 8.8, 1200000, '彼得·威尔');

INSERT INTO movies_metadata (movie_id, title, genre, year, rating, votes, director) VALUES
(1, '肖申克的救赎', '剧情', 1994, 9.7, 2778477, '弗兰克·德拉邦特'),
(2, '霸王别姬', '剧情/爱情', 1993, 9.6, 1857493, '陈凯歌'),
(3, '阿甘正传', '剧情/爱情', 1994, 9.5, 2200000, '罗伯特·泽米吉斯');

INSERT INTO ecommerce_transactions_agg (product_id, product_name, total_sales, transaction_count, avg_price) VALUES
(101, 'Laptop', 50000.00, 50, 1000.00),
(102, 'Smartphone', 30000.00, 100, 300.00),
(103, 'Headphones', 5000.00, 200, 25.00);

INSERT INTO user_behavior_agg (user_id, session_count, total_duration_seconds, avg_session_duration) VALUES
(1001, 10, 3600, 360.0),
(1002, 5, 1800, 360.0),
(1003, 8, 2880, 360.0);

INSERT INTO log_analysis_agg (hour, request_count, error_count, avg_response_time) VALUES
('2025-01-01 10:00:00', 1000, 10, 0.2),
('2025-01-01 11:00:00', 1200, 15, 0.25),
('2025-01-01 12:00:00', 1100, 12, 0.22);
'''
Date: 2025-04-07 22:17:59
LastEditors: Wang Xiaomei XianYuPigeon@outlook.com
LastEditTime: 2025-04-08 00:36:37
FilePath: /gamestats/Modules/maimai/readDB.py
'''
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def create_pool():
    # 读取环境变量
    hostname = os.getenv("DB_HOST")
    username = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    database = os.getenv("DB_DATABASE")
    port = int(os.getenv("DB_PORT", 3306))
    # 创建连接池
    pool = pymysql.ConnectionPool(
        host=hostname,
        user=username,
        password=password,
        database=database,
        port=port,
        autocommit=True,
        charset='utf8mb4'
    )
    
    return pool

class ReadUserdata:
    def input_username(account_name):
        # 创建连接池
        pool = create_pool()
        conn = pool.connection()
        cursor = conn.cursor()
        check_maimai_player_table() # 检查表是否存在
        check_account_exists(account_name) # 检查账户是否存在
        result = cursor.fetchone() # 获取结果
        cursor.close()
        conn.close()
        
        return result

def check_maimai_player_table():
        # 创建连接池
        pool = create_pool()
        
        # 从连接池获取连接
        conn = pool.connection()
        cursor = conn.cursor()
        
        try:
            # 检查表是否存在
            cursor.execute("""
                SELECT COUNT(*)
                FROM information_schema.tables
                WHERE table_schema = DATABASE()
                AND table_name = 'maimai_player'
            """)
            
            if cursor.fetchone()[0] == 0:
                # 表不存在，创建表
                cursor.execute("""
                    CREATE TABLE maimai_player (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        username VARCHAR(255) NOT NULL UNIQUE,
                        friend_code VARCHAR(20) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                    )
                """)
                print("Table maimai_player created successfully")
            else:
                print("Table maimai_player already exists")
                
        except Exception as e:
            print(f"Error checking/creating table: {e}")
        finally:
            cursor.close()
            conn.close()

@staticmethod
def check_account_exists(account_name):
    """
    检查指定的账户名是否存在于数据库中
    Args:
        account_name (str): 需要检查的账户名
    Returns:
        bool: 如果账户存在返回True，否则返回False
    """
    # 确保表存在
    check_maimai_player_table()
    
    # 创建连接池
    pool = create_pool()
    conn = pool.connection()
    cursor = conn.cursor()
    
    try:
        # 执行查询
        cursor.execute("""
            SELECT COUNT(*) 
            FROM maimai_player 
            WHERE username = %s
        """, (account_name,))
        
        count = cursor.fetchone()[0]
        return count > 0
    except Exception as e:
        print(f"检查账户存在性时出错: {e}")
        return False
    finally:
        cursor.close()
        conn.close()


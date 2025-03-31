'''
Date: 2025-03-27 23:29:07
LastEditors: Wang Xiaomei XianYuPigeon@outlook.com
LastEditTime: 2025-03-28 01:53:52
FilePath: /gamestats/Modules/maimai/getInformation.py
'''
import requests
import os
import logging
from dotenv import load_dotenv

#加载变量与机密
load_dotenv()

API_URL = "https://maimai.lxns.net/api/v0/user/maimai/player"
API_TOKEN = os.getenv("MAIMAI_API_TOKEN")
FRIEND_CODE = None #舞萌DX好友码槽位预留

#向API发送请求获取玩家信息
def get_player_status():
    headers = {
        "X-User-Token": API_TOKEN
    }
    try:
        response = requests.get(f"{API_URL}", headers=headers)
        response.raise_for_status()  # 如果响应包含错误代码则抛出异常
        
        player_data = response.json()
        return player_data
    #设置日志记录等级为WARNING
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP错误: {http_err}")
        return None
    except requests.exceptions.ConnectionError as conn_err:
        logging.error(f"连接错误: {conn_err}")
        return None
    except requests.exceptions.Timeout as timeout_err:
        logging.error(f"请求超时: {timeout_err}")
        return None
    

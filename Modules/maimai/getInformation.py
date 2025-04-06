'''
Date: 2025-03-27 23:29:07
LastEditors: Wang Xiaomei XianYuPigeon@outlook.com
LastEditTime: 2025-04-05 02:56:33
FilePath: /gamestats/Modules/maimai/getInformation.py
'''
import requests
import os
import logging
from dotenv import load_dotenv

#加载变量与机密
load_dotenv()

# API 配置
API_URL = "https://maimai.lxns.net/api/v0/maimai/player/{FRIEND_CODE}"
API_TOKEN = os.getenv("MAIMAI_API_TOKEN")
FRIEND_CODE = None #舞萌DX好友码槽位预留

#向API发送请求获取玩家信息
class PlayerStatus:
    def __init__(self, player_data):
        self.player_data = player_data
        
        # 基本信息
        self.player_id = player_data.get("player_id") # 玩家 ID
        self.player_name = player_data.get("name")  # 游戏内名称
        self.rating = player_data.get("rating", 0)  # 玩家 DX Rating
        self.friend_code = player_data.get("friend_code")  # 好友码
        self.trophy = player_data.get("trophy")  # 称号
        self.course_rank = player_data.get("course_rank")  # 段位 ID
        self.class_rank = player_data.get("class_rank")  # 阶级 ID
        self.star = player_data.get("star", 0)  # 搭档觉醒数
        self.icon = player_data.get("icon")  # 头像
        self.name_plate = player_data.get("name_plate")  # 姓名框
        self.frame = player_data.get("frame")  # 背景
        
    @staticmethod
    def get_player_status():
        headers = {
            "Authorization": API_TOKEN
        }
        try:
            response = requests.get(API_URL, headers=headers)
            response.raise_for_status()  # 如果响应包含错误代码则抛出异常
            
            player_data = response.json()
            return PlayerStatus(player_data)  # 返回PlayerStatus实例而不是原始数据
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
        except Exception as e:
            logging.error(f"未知错误: {e}")
            return None
            
    def to_dict(self):
        """将玩家数据转换为字典格式，便于其他模块使用"""
        return {
            "player_id": self.player_id,
            "name": self.player_name,
            "rating": self.rating,
            "friend_code": self.friend_code,
            "trophy": self.trophy,
            "trophy_name": self.trophy_name,
            "player_level": self.player_level,
            "player_exp": self.player_exp,
            "player_rank": self.player_rank,
            "player_score": self.player_score,
            "course_rank": self.course_rank,
            "class_rank": self.class_rank,
            "star": self.star,
            "icon": self.icon,
            "name_plate": self.name_plate,
            "frame": self.frame,
        }


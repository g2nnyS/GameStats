'''
Date: 2025-03-28 01:45:23
LastEditors: Wang Xiaomei XianYuPigeon@outlook.com
LastEditTime: 2025-04-07 23:55:03
FilePath: /gamestats/Modules/maimai/darw.py
'''

from Modules.maimai.getInformation import PlayerStatus
from PIL import *

def draw_player_status(player_status):
    #获取玩家数据
    PlayerStatus.get_player_status()
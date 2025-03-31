'''
Date: 2025-03-28 01:07:39
LastEditors: Wang Xiaomei XianYuPigeon@outlook.com
LastEditTime: 2025-03-28 01:12:32
FilePath: /gamestats/test.py
'''
import requests

def test_api():
    headers = {
        "X-User-Token": "OMh-VciBrssrgzQODOKN2JmGwZ7IaMpZdX5ywqAb2PI="
    }
    response = requests.get("https://maimai.lxns.net/api/v0/user/maimai/player", headers=headers)
    player_data = response.json()
    print(player_data)

test_api()
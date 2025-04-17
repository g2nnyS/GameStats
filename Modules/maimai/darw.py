'''
Date: 2025-03-28 01:45:23
LastEditors: Wang Xiaomei XianYuPigeon@outlook.com
LastEditTime: 2025-04-16 23:27:04
FilePath: /gamestats/Modules/maimai/darw.py
'''

import os
import requests
from io import BytesIO
from Modules.maimai.getInformation import PlayerStatus
from PIL import Image, ImageDraw, ImageFont

# 资源基础URL
BASE_URL = "https://assets2.lxns.net/maimai"
BASE_URL_2 = "https://maimai.lxns.net/assets/maimai"
# 资源缓存目录
CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache")
os.makedirs(CACHE_DIR, exist_ok=True)

def download_resource(resource_type, resource_id):
    """
    下载并缓存指定的资源
    Args:
        resource_type: 资源类型 (icon, plate, music, course_rank)
        resource_id: 资源ID
    Returns:
        BytesIO 对象或文件路径
    """
    # 构建资源URL和缓存路径
    url_map = {
        'icon': f"{BASE_URL}/icon/{resource_id}.png",
        'plate': f"{BASE_URL}/plate/{resource_id}.png",
        'course_rank': f"{BASE_URL_2}/course_rank/{resource_id}.webp",
        'class_rank': f"{BASE_URL_2}/class_rank/{resource_id}.webp",
    }
    
    url = url_map.get(resource_type)
    if not url:
        print(f"未知资源类型: {resource_type}")
        return None
    
    # 检查缓存
    cache_path = os.path.join(CACHE_DIR, f"{resource_type}_{resource_id}")
    if resource_type in ['course_rank', 'class_rank']:
        cache_path += '.webp'
    else:
        cache_path += '.png'
    
    if os.path.exists(cache_path):
        return Image.open(cache_path)
    
    # 下载资源
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        # 保存到缓存
        with open(cache_path, 'wb') as f:
            f.write(response.content)
        
        return Image.open(BytesIO(response.content))
    except Exception as e:
        print(f"下载资源失败 {resource_type}_{resource_id}: {e}")
        return None

def draw_player_status(friend_code):
    """
    获取玩家数据并绘制玩家信息卡片
    Args:
        friend_code: 玩家好友码
    Returns:
        PIL.Image: 绘制好的玩家信息图片
    """
    # 获取玩家数据
    player_status = PlayerStatus.get_player_status(friend_code)
    if not player_status or not player_status.player_data:
        print("未能获取玩家数据")
        return None
    
    # 从player_status中提取数据
    data = player_status.player_data.get('data', {})
    if not data:
        print("数据格式错误")
        return None
    
    # 创建画布，大小可以根据实际需求调整
    img_width, img_height = 1000, 500
    image = Image.new('RGBA', (img_width, img_height), (255, 255, 255, 255))
    draw = ImageDraw.Draw(image)
    try:
        # 加载字体，如果没有指定字体可以使用默认字体
        try:
            font_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts", "NotoSansSC-Regular.otf")
            title_font = ImageFont.truetype(font_path, 36)
            normal_font = ImageFont.truetype(font_path, 24)
        except Exception:
            title_font = ImageFont.load_default()
            normal_font = ImageFont.load_default()
        
        # 下载资源
        icon_img = download_resource('icon', data['icon']['id'])
        name_plate_img = download_resource('plate', data['name_plate']['id'])
        frame_img = download_resource('plate', data['frame']['id'])  # 或者使用其他特定路径
        
        # 绘制背景
        if frame_img:
            # 调整背景大小以适应画布
            frame_img = frame_img.resize((img_width, img_height))
            image.paste(frame_img, (0, 0), frame_img if frame_img.mode == 'RGBA' else None)
        
        # 绘制玩家头像
        if icon_img:
            icon_size = 100
            icon_position = (50, 50)
            icon_img = icon_img.resize((icon_size, icon_size))
            image.paste(icon_img, icon_position, icon_img if icon_img.mode == 'RGBA' else None)
        
        # 绘制玩家姓名框
        if name_plate_img:
            plate_position = (160, 45)
            image.paste(name_plate_img, plate_position, name_plate_img if name_plate_img.mode == 'RGBA' else None)
        
        # 绘制玩家信息文本
        text_start_x = 170
        text_start_y = 120
        line_height = 40
        
        # 玩家名称
        draw.text((text_start_x, text_start_y), f"名称: {data['name']}", fill=(0, 0, 0), font=title_font)
        
        # 评分
        rating_color = (255, 120, 0)  # 根据评分区间可以设置不同的颜色
        draw.text((text_start_x, text_start_y + line_height), f"Rating: {data['rating']}", fill=rating_color, font=normal_font)
        
        # 称号
        trophy_color = {'Normal': (100, 100, 100), 'Bronze': (205, 127, 50), 'Silver': (192, 192, 192), 'Gold': (255, 215, 0)}.get(data['trophy']['color'], (0, 0, 0))
        draw.text((text_start_x, text_start_y + line_height * 2), f"称号: {data['trophy']['name']}", fill=trophy_color, font=normal_font)
        
        # 段位和阶级
        course_ranks = ["无", "初心", "初级", "中级", "上级", "特级", "超特级", "超究级"]
        class_ranks = ["无", "初段", "二段", "三段", "四段", "五段", "六段", "七段", "八段", "九段", "十段", "真传"]
        
        # 下载并绘制段位图标
        course_rank_img = download_resource('course_rank', data['course_rank'])
        if course_rank_img:
            # 绘制段位图标
            course_icon_size = 50
            course_icon_position = (text_start_x - 60, text_start_y + line_height * 3)
            course_rank_img = course_rank_img.resize((course_icon_size, course_icon_size))
            image.paste(course_rank_img, course_icon_position, course_rank_img if course_rank_img.mode == 'RGBA' else None)
        
        # 仍然显示文本说明（可选）
        draw.text((text_start_x, text_start_y + line_height * 3), f"段位: {course_ranks[min(data['course_rank'], len(course_ranks)-1)]}", fill=(0, 0, 0), font=normal_font)
        draw.text((text_start_x, text_start_y + line_height * 4), f"阶级: {class_ranks[min(data['class_rank'], len(class_ranks)-1)]}", fill=(0, 0, 0), font=normal_font)
        
        # 好友码
        draw.text((text_start_x, text_start_y + line_height * 5), f"好友码: {data['friend_code']}", fill=(0, 0, 0), font=normal_font)
        
        # 星级
        draw.text((text_start_x, text_start_y + line_height * 6), f"星级: {data['star']}", fill=(0, 0, 0), font=normal_font)
        
        return image
    except Exception as e:
        print(f"绘制玩家信息时出错: {e}")
        import traceback
        traceback.print_exc()
        return None

def draw_all(friend_code, output_path="player_card.png"):
    """
    绘制完整的玩家信息卡片并保存
    Args:
        friend_code: 玩家好友码
        output_path: 输出图片路径
    Returns:
        bool: 是否成功
    """
    try:
        # 绘制玩家信息卡片
        player_card = draw_player_status(friend_code)
        if not player_card:
            return False
        
        # 保存图片
        player_card.save(output_path)
        print(f"成功生成玩家卡片: {output_path}")
        return True
    except Exception as e:
        print(f"生成玩家卡片失败: {e}")
        return False